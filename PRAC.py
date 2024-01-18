from graphlib import TopologicalSorter
from pydoc_data import topics
import tkinter
import customtkinter
import datetime as dt
import time
import threading
import random
import matplotlib.pyplot as plt
from project import calculate_all, fifo, lru, mru, optimal, random_algo   

customtkinter.set_appearance_mode("dark")  # default
customtkinter.set_default_color_theme("green")

class PageReplacementVisualizer(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.frames = []
        

        # making root window
        self.title("page replacement visualizer")
        self.geometry(f"{1100}x{580}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.textbox = tkinter.Text(self)
        self.textbox.configure(width=50, height=5)
        self.textbox.place(x=700, y=100)
        self.example = 'Welcome, to our page replacement visualiser!\n\nClick one of the buttons on the left.'

    def tksleep(self, t):
        ms = int(t * 1000)
        var = tkinter.IntVar(self)
        self.after(ms, lambda: var.set(1))
        self.wait_variable(var)

    def animated_write(self, line):
        for char in line:
            self.textbox.insert(tkinter.END, char)
            self.tksleep(0.1)
        self.textbox.insert(tkinter.END, '\n')

    def read_text(self, text):
        for line in text.splitlines():
            self.animated_write(line)

        # making side frame for mode widgets/ live time and date
        self.sidebar = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")

        # live date"
        self.date = dt.datetime.now()
        self.date_label = customtkinter.CTkLabel(self.sidebar, text=f"{self.date:%A, %B %d ,%Y}")
        self.date_label.grid(row=10, column=0)

        # live time
        self.timer_font = customtkinter.CTkFont(family='Helvetica', size=14)
        self.timer = customtkinter.CTkTextbox(self, width=95, height=30, border_width=0, font=self.timer_font)
        self.timer.insert("0.0", "")
        self.timer.place(x=115, y=470)

        # top label for sidebar, page replacement algos in homepage
        self.heading = customtkinter.CTkLabel(self.sidebar, text="Page Replacement Algorithms",
                                              font=customtkinter.CTkFont(size=20, weight="bold"))
        self.heading.grid(row=0, column=0, padx=20, pady=(20, 10))

        # mode- dark/light-gui part
        self.mode_label = customtkinter.CTkLabel(self.sidebar, text="Appearance Mode")
        self.mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.mode_menu = customtkinter.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"],
                                                     command=self.appearance)
        self.mode_menu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # 5 page replacement buttons , LRU, MRU, Optimal, Random , fifo , compare algos
        self.LRU = customtkinter.CTkButton(self.sidebar, text='LRU', command=lambda: self.run_algorithm('LRU'))
        self.LRU.grid(row=1, column=0, padx=20, pady=10)
        self.FIFO = customtkinter.CTkButton(self.sidebar, text='FIFO', command=lambda: self.run_algorithm('FIFO'))
        self.FIFO.grid(row=2, column=0, padx=20, pady=10)
        self.Random = customtkinter.CTkButton(self.sidebar, text='Random', command=lambda: self.run_algorithm('Random'))
        self.Random.grid(row=4, column=0, padx=20, pady=10)
        self.Optimal = customtkinter.CTkButton(self.sidebar, text='Optimal', command=lambda: self.run_algorithm('Optimal'))
        self.Optimal.grid(row=5, column=0, padx=20, pady=10)
        # Run the clock in the main thread
        self.clock()

    def clock(self):
        hour = time.strftime("%r")
        self.timer.delete("0.0", "end")
        self.timer.insert("0.0", hour)
        self.after(1000, self.clock)  # Schedule the next update in 1000 milliseconds (1 second)

    def run_algorithm(self, algorithm):
        
        top = tkinter.Toplevel()
        top.title(f'{algorithm} page replacement')
        top.geometry(f"{1100}x{580}")
        top.grid_columnconfigure(1, weight=1)
        top.grid_columnconfigure((2, 3), weight=0)
        top.grid_rowconfigure((0, 1, 2), weight=1)
        # defining an entry box to accept the number of frames
        top.frame_entry = customtkinter.CTkEntry(top, placeholder_text="frame number", width=288, height=28)
        top.frame_entry.place(x=200, y=100)
        # defining an entry box to accept the reference string separated by spaces
        top.ref_entry = customtkinter.CTkEntry(top, placeholder_text="reference string", width=288, height=28)
        top.ref_entry.place(x=200, y=200)
        # back button
        top.back_button = customtkinter.CTkButton(top, text="Back", command=lambda: self.backfn(top))
        top.back_button.place(x=100, y=500)
        # visualise button
        top.visualise_button = customtkinter.CTkButton(top, text='visualise',
                                                       command=lambda: self.table_animation(top,algorithm))
        top.visualise_button.place(x=350, y=500)
        top.Plot_graph = customtkinter.CTkButton(top, text = "Graph", command=lambda: self.plot_graph(top))
        top.Plot_graph.place(x=550, y=500)
        top.comp_button=customtkinter.CTkButton(top,text="compare all algorithms",command= lambda: self.comp(top))
        top.comp_button.place(x=750, y=500)
        top.mainloop()
        
    def submit_action(self, top, algorithm):
        try:
            frame_count=int(top.frame_entry.get())
        except ValueError:
            return
        self.num_frames = frame_count  # Storing the frame count
        self.reference_string = top.ref_entry.get().split()
        top.hit_ratio_label = customtkinter.CTkLabel(top, text="")
        top.miss_ratio_label=customtkinter.CTkLabel(top, text="")
        top.result_label = customtkinter.CTkLabel(top, text="")
        frames = list(range((frame_count)))
        reference_string = top.ref_entry.get().split()
        result, hit_ratio = self.run_page_replacement_algorithm(algorithm,frames, reference_string)

        top.hit_ratio_label.configure(text=f"Hit ratio:{hit_ratio:.2f}",fg='black')
        top.miss_ratio_label.configure(text=f"Miss ratio:{1-hit_ratio:.2f}",fg='black')
        top.hit_ratio_label.place(x=200, y=300)
        top.result_label.configure(text=f"result:{result}")
        top.result_label.place(x=200, y=320)

    def backfn(self, top):
        top.destroy()
    def plot_graph(self, top):
        num_frames = int(top.frame_entry.get())
        page_references = [int(x) for x in top.ref_entry.get().split(' ')]
        algorithms = ['FIFO', 'LRU', 'MRU', 'Random', 'Optimal']
        algorithm_var = customtkinter.StringVar(top)
        algorithm_var.set(algorithms[0]) 
        selected_algorithm = algorithm_var.get()
        results = calculate_all(page_references, num_frames)

        frame_values = list(results.keys())
        hit_ratios = [results[frame][0] for frame in frame_values]
        miss_ratios = [results[frame][1] for frame in frame_values]

        plt.figure(figsize=(8, 6))
        plt.plot(frame_values, hit_ratios, label='Miss Ratio')
        plt.xlabel('Number of Frames')
        plt.ylabel('Miss Ratio')
        plt.title('Miss Ratio')#title
        plt.legend()

        plt.figure(figsize=(8, 6))
        plt.plot(frame_values, miss_ratios, label='Hit Ratio')
        plt.xlabel('Number of Frames')
        plt.ylabel('Hit Ratio')
        plt.title('Hit Ratio')#title
        plt.legend()

        plt.show()
    
    def table_animation(self,top,algorithm):
        num_frames = int(top.frame_entry.get())
        page_references = [int(x) for x in top.ref_entry.get().split(' ')]
        #algorithm = self.algorithm_choice.get()
        animate_window = tkinter.Toplevel()
        animate_window.title("Visualization Window")
        animate_window.geometry(f"{1100}x580")
        animate_window.mycanvas = tkinter.Canvas(animate_window, width=300, height=100, bg='white')
        animate_window.mycanvas.pack(fill=tkinter.BOTH, expand=True)
        
        canvas_frame = tkinter.Frame(animate_window)
        canvas_frame.pack(fill=tkinter.BOTH, expand=True)
        animate_window.mycanvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        scrollbar = tkinter.Scrollbar(canvas_frame, orient=tkinter.VERTICAL, command=animate_window.mycanvas.yview)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        animate_window.mycanvas.config(yscrollcommand=scrollbar.set)
        
        frames = [-1] *num_frames
        hits = ['✓' if i == 1 else '✗' for i in range(len(page_references))]

        x_offset = 30
        y_offset = 50
        rect_width = 50
        rect_height = 50
        spacing = 10
        miss_ratio_label = tkinter.Label(
        animate_window,
        text="Miss Ratio: 0%",
        font=("Arial", 14, "bold")
    )
        hit_ratio_label = tkinter.Label(
        animate_window,
        text="Hit Ratio: 0%",
        font=("Arial", 14, "bold")
    )
        hit_ratio_label.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)
        miss_ratio_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        for i in range(num_frames):
            animate_window.mycanvas.create_text(
            x_offset + (i + 1) * (rect_width + spacing) + (rect_width // 2),
            y_offset - 20,
            text="FRAME " + str(i + 1)
            
        )
        miss_count = 0
        hit_count = 0

        total_references = len(page_references)
        page_queue = []  # For FIFO
        lru_dict = {}  # For LRU
        random_list = []  # For Random
        optimal_list = []  # For Optimal

        for i, ref in enumerate(page_references):
           
            hit_text = hits[i]
            ref_text = ref

            animate_window.mycanvas.create_rectangle(
                x_offset, y_offset, x_offset + rect_width, y_offset + rect_height, outline="black"
            )
            animate_window.mycanvas.create_text(
                x_offset + (rect_width // 2), y_offset + (rect_height // 2), text=ref_text
            )
            animate_window.mycanvas.create_text(
                x_offset + rect_width + 25, y_offset + (rect_height // 2), text=hit_text
            )

            if algorithm == 'FIFO':
                if ref not in frames:
                    miss_count += 1
                    #hit_count = 100 - miss_count
                # Update miss ratio label
                    miss_ratio = (miss_count / total_references) * 100 if total_references > 0 else 0
                    miss_ratio_label.config(text=f"Miss Ratio: {miss_ratio:.2f}%")
                    
                # Update hit ratio label
                    hit_ratio = 100 - miss_ratio
                    hit_ratio_label.config(text=f"Hit Ratio: {hit_ratio:.2f}%")
                    if len(page_queue) < num_frames:
                        page_queue.append(ref)
                        frames[len(page_queue) - 1] = ref
                    else:
                        popped_page = page_queue.pop(0)
                        frames[frames.index(popped_page)] = ref
                        page_queue.append(ref)

            elif algorithm == 'LRU':
                if ref not in frames:
                    miss_count += 1
                   # hit_count = 1 - miss_count
                # Update miss ratio label
                    miss_ratio = (miss_count / total_references) * 100 if total_references > 0 else 0
                    miss_ratio_label.config(text=f"Miss Ratio: {miss_ratio:.2f}%")
                    
                # Update hit ratio label
                    hit_ratio =  100 - miss_ratio
                    hit_ratio_label.config(text=f"Hit Ratio: {hit_ratio:.2f}%")
                    if len(lru_dict) < num_frames:
                        lru_dict[ref] = i
                        frames[len(lru_dict) - 1] = ref
                    else:
                        least_recent = min(lru_dict, key=lru_dict.get)
                        lru_dict.pop(least_recent)
                        frames[frames.index(least_recent)] = ref
                        lru_dict[ref] = i

            elif algorithm == 'Random':
                if ref not in frames:
                    miss_count += 1
                  
                # Update miss ratio label
                    miss_ratio = (miss_count / total_references) * 100 if total_references > 0 else 0
                    miss_ratio_label.config(text=f"Miss Ratio: {miss_ratio:.2f}%")
                    
                # Update hit ratio label
                    hit_ratio = 100 - miss_ratio
                    hit_ratio_label.config(text=f"Hit Ratio: {hit_ratio:.2f}%")
                    if len(random_list) < num_frames:
                        random_list.append(ref)
                        frames[len(random_list) - 1] = ref
                    else:
                        frames[random.randint(0, num_frames - 1)] = ref

            elif algorithm == 'Optimal':
                if ref not in frames:
                    miss_count += 1
                    
                # Update miss ratio label
                    miss_ratio = (miss_count / total_references) * 100 if total_references > 0 else 0
                    miss_ratio_label.config(text=f"Miss Ratio: {miss_ratio:.2f}%")
                    
                # Update hit ratio label
                    hit_ratio = 100 - miss_ratio
                    hit_ratio_label.config(text=f"Hit Ratio: {hit_ratio:.2f}%")
                    if len(optimal_list) < num_frames:
                        optimal_list.append(ref)
                        frames[len(optimal_list) - 1] = ref
                    else:
                        indexes = {frame: page_references[i:].index(frame) if frame in page_references[i:] else float('inf')
                                   for frame in frames}
                        farthest_page = max(indexes, key=indexes.get)
                        frames[frames.index(farthest_page)] = ref
                        
            for j, frame in enumerate(frames):
                fill_color = "pink"
                if frame == int(ref):
                    fill_color = "pink" if hit_text == '✓' else "pink"
                animate_window.mycanvas.create_rectangle(
                    x_offset + (j + 1) * (rect_width + spacing),
                    y_offset, x_offset + (j + 1) * (rect_width + spacing) + rect_width,
                    y_offset + rect_height, outline="black", fill=fill_color
                )
                animate_window.mycanvas.create_text(
                    x_offset + (j + 1) * (rect_width + spacing) + (rect_width // 2),
                    y_offset + (rect_height // 2), text=str(frame) if frame != -1 else ""
                )

            y_offset += rect_height + spacing

        animate_window.mainloop()
        return
    def comp(self,top):

        top.comp_graph_button=customtkinter.CTkButton(top,text="generate a comparison graph",command=lambda: self.plotcomparison(top),width=100, height=100)
        top.comp_graph_button.place(x=600, y=100)

        frames11=int(top.frame_entry.get())
        reference_string11 = top.ref_entry.get().split()

        top.hl1=customtkinter.CTkLabel(top,text="")
        top.ml1=customtkinter.CTkLabel(top,text="")
        top.hl2=customtkinter.CTkLabel(top,text="")
        top.ml2=customtkinter.CTkLabel(top,text="")
        top.hl3=customtkinter.CTkLabel(top,text="")
        top.ml3=customtkinter.CTkLabel(top,text="")
        top.hl4=customtkinter.CTkLabel(top,text="")
        top.ml4=customtkinter.CTkLabel(top,text="")
        top.hl5=customtkinter.CTkLabel(top,text="")
        top.ml5=customtkinter.CTkLabel(top,text="")

        #frames11- number of frames, hr- hit ratio , res- miss ratio
        mr1,hr1=lru(reference_string11,frames11)
        mr2,hr2=fifo(reference_string11,frames11)
        mr3,hr3=mru(reference_string11,frames11)
        mr4,hr4=optimal(reference_string11,frames11)
        mr5,hr5=random_algo(reference_string11,frames11)

    

        top.hl1.configure(text=f"LRU hit ratio:{hr1:.2f}")
        top.hl1.place(x=200,y=280)
        top.ml1.configure(text=f"LRU miss ratio:{mr1:.2f}")
        top.ml1.place(x=200,y=300)

        top.hl2.configure(text=f"FIFO hit ratio:{hr2:.2f}")
        top.hl2.place(x=200,y=320)
        top.ml2.configure(text=f"FIFO miss ratio:{mr2:.2f}")
        top.ml2.place(x=200,y=340)

        top.hl3.configure(text=f"MRU hit ratio:{hr3:.2f}")
        top.hl3.place(x=200,y=360)
        top.ml3.configure(text=f"MRU miss ratio:{mr3:.2f}")
        top.ml3.place(x=200,y=380)

        top.hl4.configure(text=f"Optimal hit ratio:{hr4:.2f}")
        top.hl4.place(x=200,y=400)
        top.ml4.configure(text=f"Optimal miss ratio:{mr4:.2f}")
        top.ml4.place(x=200,y=420)

        top.hl5.configure(text=f"Random hit ratio:{hr5:.2f}")
        top.hl5.place(x=200,y=440)
        top.ml5.configure(text=f"Random miss ratio:{mr5:.2f}")
        top.ml5.place(x=200,y=460)
    def plotcomparison(self,top):
        frames=int(top.frame_entry.get())
        ref_string=top.ref_entry.get().split()
        res1,hr1=lru(ref_string,frames)
        res2,hr2=fifo(ref_string,frames)
        res3,hr3=mru(ref_string,frames)
        res4,hr4=optimal(ref_string,frames)
        res5,hr5=random_algo(ref_string,frames)
        #x axis- algorithms
        #y axis- hit ratio
        algos=['LRU','FIFO','MRU','Optimal','Random']
        hr=[hr1,hr2,hr3,hr4,hr5]
        miss=[res1,res2,res3,res4,res5]
        plt.plot(algos,hr)
        plt.plot(algos,miss)
        plt.xlabel('algorithms')
        plt.ylabel('hit ratio')
        plt.title('comparison line graph')
        plt.show()
    def run_page_replacement_algorithm(self, algorithm, frames, reference_list):
        result = f"Running {algorithm} algorithm with {frames} frames and reference list {reference_list}"
        hit_count = 0

        if algorithm == 'LRU':
            frames_order = []
            for page in reference_list:
                if page in frames_order:
                    frames_order.remove(page)
                frames_order.insert(0, page)
                if page in frames:
                    hit_count += 1
                else:
                    frames.pop()
                    frames.insert(0, page)
        elif algorithm == 'FIFO':
            frames_queue = []
            for page in reference_list:
                if page in frames:
                    hit_count += 1
                else:
                    if len(frames_queue) == len(frames):
                        frames.remove(frames_queue.pop(0))
                    frames_queue.append(page)
                    frames.append(page)
        elif algorithm == 'Optimal':
            future_pages = reference_list[:]
            for page in reference_list:
                if page in frames:
                    hit_count += 1
                else:
                    if len(frames) < len(future_pages):
                        frames.append(page)
                    else:
                        farthest_page = max(future_pages, key=lambda x: future_pages.index(x) if x in frames else float('inf'))
                        frames[frames.index(farthest_page)] = page
                        future_pages.pop(0)
        elif algorithm == 'Random':
            for page in reference_list:
                if page in frames:
                    hit_count += 1
                else:
                    random_page = random.choice(frames)
                    frames[frames.index(random_page)] = page

        if not reference_list:
            return result, 0.0

        hit_ratio = hit_count / len(reference_list)
        miss_count = 1-hit_count
        return result, round(hit_ratio, 2)
    
        
    def appearance(self, newmode: str):
        customtkinter.set_appearance_mode(newmode)


if __name__ == "__main__":
    root = PageReplacementVisualizer()
    root.read_text(root.example)
    root.mainloop()
