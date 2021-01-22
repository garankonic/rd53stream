import sys
import os
sys.path.append(os.path.abspath("."))
import pyrd53.pybindings
import shutil
import psutil

if len(sys.argv) < 2:
    print("Mr./Mrs. you have to specify the name of the input file")
else:
    # get file
    filename = sys.argv[1]
    nevents = int(sys.argv[2]) if (len(sys.argv) > 2) else 0
    enc = pyrd53.pybindings.EventEncoder(filename)
    # create output folder
    outputfolder = filename.split("/")[-1].split(".")[0]
    outputfolder = "./processed_streams/"+outputfolder
    if os.path.exists(outputfolder):
        shutil.rmtree(outputfolder)
    os.mkdir(outputfolder)
    # start
    event_counter = 0
    chip_counter = 0
    skip_counter = 0
    split_counter = 0
    while True:
        print("Event # ", event_counter)
        ev = enc.get_next_event(False)
        if(not ev.is_empty()):
            ch = ev.get_next_chip()
            while (len(ch[1]) > 0):
                # check mismatch
                raw_hits_with_adc = ev.get_chip_hits(ch[0])
                cluster_hits = []
                for cluster in ev.get_chip_clusters(ch[0]):
                    cluster_hits += cluster.get_hits()
                match = (len(raw_hits_with_adc) == len(cluster_hits))
                if (not match):
                    print("\t\tNumber of RAW and Cluster hits does not match, skipping this chip")
                    skip_counter += 1
                else:
                    f = open(outputfolder+"/stream_"+ch[0].identifier_str()+".txt", "a")
                    stream_line = str(ev.get_event_id_raw()) + "\t" + str(ev.get_chip_nclusters(ch[0]))
                    for stream_word in ch[1]:
                        stream_line += ("\t" + str(stream_word))
                    stream_line += "\n"
                    f.write(stream_line)
                    f.close()
                    # increment count
                    chip_counter += 1
                    # increment split
                    if ev.get_chip_was_split(ch[0]):
                        split_counter += 1
                # get next
                ch = ev.get_next_chip()
            # increment event counter
            event_counter += 1
        else:
            break
        # break mechanism
        if nevents > 0 and event_counter >= nevents:
            break
    info_string = ("Processing done. Total events: " + str(event_counter) + ". Total chips: " + str(chip_counter) + "\n")
    info_string += ("Chips had split: " + str(split_counter) + "\n")
    info_string += ("Chips skipped: " + str(skip_counter) + "\n")
    print(info_string)
    f = open(outputfolder + "/00_info.txt", "w+")
    f.write(info_string)
    f.close()

