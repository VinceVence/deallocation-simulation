# Deallocation Simulation

`Deallocation` is simply defined as freeing an allocated memory space. Deallocating varies per system and the approaches may differ depending on the available Job Status of the memory blocks. A process has to be loaded into the RAM for its execution and remains in the RAM until its completion. Finished processes are deallocated or removed from the memory and new processes are allocated again. This is how the OS works with allocation and deallocation.

In high-level, programming memory deallocation is done by garbage collection. The absence of this in low-level programming makes deallocation even more necessary. There are different kinds of memory models that have different deallocation techniques.

**For fixed-partition system:**
* Straightforward process
* When job completes, Memory Manager resets the status of the job's memory block to "free".
* Any code--for example, binary values with 0 indicating free and 1 indicating busy--may be used.

**For dynamic-partition system:**
* Algorithm tries to combine free areas of memory whenever possible.
* Three cases:
  * **Case 1:** When the block to be deallocated is adjacent to another free block.
  * **Case 2:** When the block to be deallocated is between two free blocks.
  * **Case 3:** When the block to be deallocated is isolated from other free blocks.  


This simulations aims to give a visual overview of how deallocation works for both systems through the Python Programming Language.

## Shared Resources
You can find the website of the simulation [here](https://vincevence-deallocation-simulation-web-app-k9jw7d.streamlitapp.com/). The accompanying website can be accessed through this [link](https://colab.research.google.com/drive/1uVqW8jmV1NY3yie23zOd5iDJL9NSbbyy?usp=sharing).

## Importing Necessary Libraries
In this simulation, the dependencies that will be utilized are as follows:

* **NumPy:** NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays.
* **Pandas:** Pandas is a software library written for the Python programming language for data manipulation and analysis. In particular, it offers data structures and operations for manipulating numerical tables and time series.
* **Matplotlib:** Matplotlib is a plotting library for the Python programming language and its numerical mathematics extension NumPy. It provides an object-oriented API for embedding plots into applications using general-purpose GUI toolkits like Tkinter, wxPython, Qt, or GTK.
* **IPython:** IPython is a command shell for interactive computing in multiple programming languages, originally developed for the Python programming language, that offers introspection, rich media, shell syntax, tab completion, and history. 
* **Time:** The time() function returns the number of seconds passed since epoch.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the neccessary libraries.

```bash
# Installing the libraries
!pip install numpy
!pip install pandas
!pip install matplotlib
!pip install IPython
```

## Fixed-Partition Systems Deallocation
This is the oldest and simplest technique used to put more than one process in the main memory. In this partitioning, the number of partitions (non-overlapping) in RAM is fixed but the size of each partition may or may not be the same. As it is a contiguous allocation, hence no spanning is allowed. Here partitions are made before execution or during system configure. 

### Generating random memory block for fixed partition system

**📝Note:** In the following cell, notice that there is a method called `np.random.seed(42)` placed above the generating function assignment. This just ensures that the generated block will produce the same output regardless of who runs the code. This is done for reproduction purposes and feel free to remove the code for generating your own randomized block.

```python
# Generate random memory block
np.random.seed(RANDOM_SEED)
df = generate_fixed_partition_dataframe(NUM_JOBS)
```
### Deallocating Fixed Partition
To deallocate the generated memory block for fixed partition system, just call the `deallocate_fixed_partition(df)` function and put the generated DataFrame as parameter. This will return the time latency it took to deallocate the block.

```python
time_latency = deallocate_fixed_partition(df)
```

## Dyamic-Partition Systems Deallocation

Dynamic partitioning tries to overcome the problems caused by fixed partitioning. In this technique, the partition size is not declared initially. It is declared at the time of process loading.

The first partition is reserved for the operating system. The remaining space is divided into parts. The size of each partition will be equal to the size of the process. The partition size varies according to the need of the process so that the internal fragmentation can be avoided.

### Generating random memory block for dynamic partition system

**📝Note:** In the following cell, notice that there is a method called `np.random.seed(42)` placed above the generating function assignment. This just ensures that the generated block will produce the same output regardless of who runs the code. This is done for reproduction purposes and feel free to remove the code for generating your own randomized block.

```python
# Generate random dataframe
np.random.seed(RANDOM_SEED)
df = generate_dynamic_partition_dataframe(NUM_JOBS)
```

### Deallocating Dynamic Partition Case 1
To deallocate the generated memory block for dynamic partition system case 1, just call the `deallocate_dynamic_case_1(df)` function and put the generated DataFrame as parameter. This will return the time latency it took to deallocate the block.

```python
# Deallocating for every possible iterations using the case 1 parameters
time_latency_case_1 = deallocate_dynamic_case_1(df, one_iter=True)
```
### Deallocating Dynamic Partition Case 2
To deallocate the generated memory block for dynamic partition system case 2, just call the `deallocate_dynamic_case_2(df)` function and put the generated DataFrame as parameter. This will return the time latency it took to deallocate the block.

```python
# Deallocating for every possible iterations using the case 2 parameters
time_latency_case_2 = deallocate_dynamic_case_2(df, remove_null=True)
```

### Deallocating Dynamic Partition Case 3
To deallocate the generated memory block for dynamic partition system case 3, just call the `deallocate_dynamic_case_3(df)` function and put the generated DataFrame as parameter. This will return the time latency it took to deallocate the block.

```python
# Deallocating for every possible iterations using the case 3 parameters
time_latency_case_3 = deallocate_dynamic_case_3(df)
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Support
For any queries or issues regarding the source code, don't hesitate to contact me on the following email: `lanz.vencer@lpunetwork.edu.ph`

## License
[MIT](https://choosealicense.com/licenses/mit/)