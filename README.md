# **Banker's Algorithm Implementation using Python**

This is a Python program that implements the **Banker's algorithm**, which is used to avoid deadlock in a computer system with multiple processes competing for a finite set of resources by determining whether a request for resources can be safely granted. The program uses **PyQt5** to create a graphical user interface (GUI) for the user to input the necessary data and visualize the output.

## **How to use**

To use this program, simply run code in a Python environment that has **PyQt5** and **NumPy** installed. Once the program is running, you will be presented with a window asking for the number of resources and processes.

After entering the required information, click "Next" to proceed to the next windows where you can enter and submit the current allocation, maximum need, and total resources.

Then, a window will appear where you can request additional resource for a certain process. Finally, the result of the Banker's Algorithm will be displayed.

## **Example Pictures**

You can find below some example pictures of the GUI input screens:

![GUI Input](../Example/Example1-1.png)
*Example of input screen*

![GUI Input](../Example/Example1-2.png)
*Example of input screen*

![GUI Input](../Example/Example1-3.png)
*Example of input screen*

![GUI Input](../Example/Example1-4.png)
*Example of input screen*

![GUI Input](../Example/Example1-5.png)
*Example of input screen*

![GUI Input](../Example/Example1-6.png)
*Example of input screen*

## **Implementation Details**

The program is implemented using **PyQt5**, which provides a framework for building desktop applications with Python which is used for creating windows, buttons, text boxes, and other widgets.

The algorithm itself is implemented using **NumPy** arrays to represent the resource state at different points in time. The `Banker` class contains the logic for determining whether a request for resources can be safely granted.

Overall, the program provides a simple way to demonstrate the workings of the **Banker's Algorithm**.
