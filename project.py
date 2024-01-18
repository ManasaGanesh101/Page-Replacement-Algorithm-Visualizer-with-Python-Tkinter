import tkinter as tk
import matplotlib.pyplot as plt
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function for FIFO algorithm
def fifo(page_references, num_frames):
    frame_set = set()
    page_faults = 0
    page_fault_sequence = []

    for page in page_references:
        if len(frame_set) < num_frames:
            if page not in frame_set:
                frame_set.add(page)
                page_faults += 1
        else:
            if page not in frame_set:
                frame_set.remove(page_fault_sequence.pop(0))
                frame_set.add(page)
                page_faults += 1

        page_fault_sequence.append(page)

    return page_faults / len(page_references), (len(page_references) - page_faults) / len(page_references)

# Function for LRU algorithm
def lru(page_references, num_frames):
    frame_list = []
    page_faults = 0
    page_fault_sequence = []

    for page in page_references:
        if page in frame_list:
            frame_list.remove(page)
            frame_list.append(page)
        else:
            if len(frame_list) < num_frames:
                frame_list.append(page)
            else:
                frame_list.pop(0)
                frame_list.append(page)
            page_faults += 1

        page_fault_sequence.append(page)

    return page_faults / len(page_references), (len(page_references) - page_faults) / len(page_references)

# Function for MRU algorithm
def mru(page_references, num_frames):
    frame_list = []
    page_faults = 0
    page_fault_sequence = []

    for page in page_references:
        if page in frame_list:
            frame_list.remove(page)
            frame_list.append(page)
        else:
            if len(frame_list) < num_frames:
                frame_list.append(page)
            else:
                frame_list.pop()
                frame_list.append(page)
            page_faults += 1

        page_fault_sequence.append(page)

    return page_faults / len(page_references), (len(page_references) - page_faults) / len(page_references)

# Function for Random algorithm
def random_algo(page_references, num_frames):
    frame_list = []
    page_faults = 0
    page_fault_sequence = []

    for page in page_references:
        if page in frame_list:
            pass
        else:
            if len(frame_list) < num_frames:
                frame_list.append(page)
            else:
                frame_list[random.randint(0, num_frames - 1)] = page
            page_faults += 1

        page_fault_sequence.append(page)

    return page_faults / len(page_references), (len(page_references) - page_faults) / len(page_references)

# Function for Optimal algorithm
def optimal(page_references, num_frames):
    frame_list = []
    page_faults = 0
    page_fault_sequence = []

    for i, page in enumerate(page_references):
        if page in frame_list:
            pass
        else:
            if len(frame_list) < num_frames:
                frame_list.append(page)
            else:
                indexes = {frame: page_references[i:].index(frame) if frame in page_references[i:] else float('inf')
                           for frame in frame_list}
                farthest_page = max(indexes, key=indexes.get)
                frame_list[frame_list.index(farthest_page)] = page
            page_faults += 1

        page_fault_sequence.append(page)

    return page_faults / len(page_references), (len(page_references) - page_faults) / len(page_references)

# Function to calculate hit and miss ratios for all algorithms
def calculate_all(page_references, num_frames):
    algorithms = {
        'FIFO': fifo(page_references, num_frames),
        'LRU': lru(page_references, num_frames),
        'MRU': mru(page_references, num_frames),
        'Random': random_algo(page_references, num_frames),
        'Optimal': optimal(page_references, num_frames)
    }

    return algorithms
