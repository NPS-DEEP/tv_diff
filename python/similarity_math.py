from collections import defaultdict
from math import ceil, floor
from settings_store import texture_compatible
import statistics

"""
Calculates similarity lines, histograms, and statistics.
"""

# Return compensated histogram where the right slope part is flipped and added
# to the left slope part.
def _compensated_histogram(size1, size2, histogram):

    if size1 + size2 == 0:
        return list(),list()

    # ordered size
    large = size1
    small = size2
    if small > large:
        large,small = small,large

    # number of slope buckets
    num_buckets = len(histogram)
    num_left_slope_buckets = int(num_buckets * small/(large+small) + 0.49)

    # compensated histogram
    compensated_histogram = histogram[:-num_left_slope_buckets]
    j = num_buckets - num_left_slope_buckets
    for i in range(num_left_slope_buckets):
        compensated_histogram[i] += histogram[j+i]

    # mean power
    mean_power = statistics.mean(histogram)
    max_mean_power = mean_power * ((large+small)/large)
    mean_power_histogram = [max_mean_power]*num_buckets
    for i in range(num_left_slope_buckets):
        local_mean = max_mean_power * i / num_left_slope_buckets
        mean_power_histogram[i] = local_mean
        mean_power_histogram[-i] = local_mean

    return compensated_histogram, mean_power_histogram

# get num_buckets and sections_per_bucket
def _bucket_info(section_size, step, file_size1, file_size2):
    total_sections = ceil((file_size1 + file_size2) / section_size)
    sections_per_bucket = ceil(total_sections / step / 500) * step
    num_buckets = ceil(total_sections / sections_per_bucket)
    num_f1_sections = file_size1 / section_size # float
    return num_buckets, sections_per_bucket, num_f1_sections

# for compensated histogram
def _histogram_stats(histogram):
    # histogram mean and SD, SD requires at least 2 data points
    if len(histogram) >= 2:
        sd = statistics.stdev(histogram)
        mean = statistics.mean(histogram)
        maxv = max(histogram)
        sumv = sum(histogram)
    else:
        sd = 0.0
        mean = 0.0
        maxv = 0
        sumv = 0
    return sd, mean, maxv, sumv

def empty_similarity_data():
    empty_data = dict()
    empty_data["similarity_lines"] = dict()
    empty_data["similarity_histogram"] = list()
    empty_data["compensated_histogram"] = list()
    empty_data["mean_power_histogram"] = list()
    empty_data["sd"] = 0.0
    empty_data["mean"] = 0.0
    empty_data["max"] = 0
    empty_data["sum"] = 0
    return empty_data

# return data structures given inputs
def generate_similarity_data(tv_data1, tv_data2, step,
                             settings, use_similarity_lines):

    # validate input
    if not tv_data1 or not tv_data2:
        # no data
        return empty_similarity_data()
    if not texture_compatible(settings["names"], tv_data1["texture_names"]):
        raise Exception("Incompatible tv data in file 1")
    if not texture_compatible(settings["names"], tv_data2["texture_names"]):
        raise Exception("Incompatible tv data in file 2")
    if not tv_data1["section_size"] == tv_data2["section_size"]:
        raise Exception("Incompatible tv data: secton size mismatch.")
    if step < 1:
        raise Exception("Bad")

    # calculate bucket numbers for even section distribution
    num_buckets, sections_per_bucket, num_f1_sections = _bucket_info(
                               tv_data1["section_size"], step,
                               tv_data1["file_size"], tv_data2["file_size"])

    # similarity lines and similarity histogram
    similarity_lines = defaultdict(list)
    similarity_histogram = [0]*num_buckets

    # optimization
    use = settings["use"]

    use0 = use[0]
    use1 = use[1]
    use2 = use[2]
    use3 = use[3]
    use4 = use[4]

    threshold = settings["threshold"]
    t0 = threshold[0]
    t1 = threshold[1]
    t2 = threshold[2]
    t3 = threshold[3]
    t4 = threshold[4]

    data1 = tv_data1["texture_vectors"]
    data2 = tv_data2["texture_vectors"]

    if not(use0 or use1 or use2 or use3 or use4):
        return empty_similarity_data()

    # histogram numbers
    file_size1 = tv_data1["file_size"]
    file_size2 = tv_data2["file_size"]
    section_size = tv_data1["section_size"]

    # find similarity lines
    for i in range(0, len(data1), step):
        for j in range(0, len(data2), step):
            if use0 and abs(data1[i][0] - data2[j][0]) > t0:
                continue
            if use1 and abs(data1[i][1] - data2[j][1]) > t1:
                continue
            if use2 and abs(data1[i][2] - data2[j][2]) > t2:
                continue
            if use3 and abs(data1[i][3] - data2[j][3]) > t3:
                continue
            if use4 and abs(data1[i][4] - data2[j][4]) > t4:
                continue

            # maybe add point to similarity lines
            if use_similarity_lines:
                similarity_lines[i].append(j)

            # add point to similarity histogram
            bucket = int((j - i + num_f1_sections) / sections_per_bucket)
            similarity_histogram[bucket] += 1

    # prepare compensated and mean power histograms
    compensated_histogram, mean_power_histogram = _compensated_histogram(
                           file_size1, file_size2, similarity_histogram)

    # prepare histogram statistics
    sd, mean, maxv, sumv = _histogram_stats(compensated_histogram)

    # build similarity data
    similarity_data = dict()
    if use_similarity_lines:
        similarity_data["similarity_lines"] = similarity_lines
    similarity_data["similarity_histogram"] = similarity_histogram
    similarity_data["compensated_histogram"] = compensated_histogram
    similarity_data["mean_power_histogram"] = mean_power_histogram
    similarity_data["sd"] = sd
    similarity_data["mean"] = mean
    similarity_data["max"] = maxv
    similarity_data["sum"] = sumv

    return similarity_data

