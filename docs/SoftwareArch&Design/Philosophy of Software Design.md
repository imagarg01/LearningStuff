# Notes

- The most fundamental problem in computer science is problem decomposition: hot to take a complex problem and break it down into manageable pieces that can be solved independently and then recombined to solve the original problem.

- All programming requires is a creative mind and the ability to organize your thoughts. If you can visualize a solution, you can program it.

- Simpler designs are easier to understand, easier to implement, and easier to maintain.

- There are two ways to make a program simpler: reduce the number of parts or reduce the complexity of each part.

1. Complexity can be reduced by eliminating unnecessary parts or by reducing the complexity of individual parts.
2. Second approach is to encapsulate it, so that programmers can work on a system without being exposed to all of its complexity at once. This approach is called modularization.

- Incremental development means that software design is never finished. Instead, it is a continuous process of improvement. Designs are always evolving, and there is always room for improvement. Developer should always be thinking about how to make the design simpler and better. The initial design is just a starting point and almost never the best design.

- One of the best ways to improve your design skills is to learn to recognize red flags. When you see a red flag, stop and look for an alternative design that eliminates the problem.

- Complexity is anything related to the structure of a software system that makes it hard to understand, modify, or extend.
  There are many forms:

1. Hard to understand how a piece of code works.
2. Lots of effort to make a small change or it might not be clear which parts of the system must be changed to implement a new feature; it might be difficult to fix one bug without introducing another.

Overall complexity of a system is determined by the complexity of its parts and the interactions between those parts. Also time spent by developer on that part. **Complexity is more apparent to readers than writers.**

- **Symptoms of Complexity**:

1. **Change amplification**: A small change requires many changes or change at many places. One of the goal of good design is to minimize change amplification, reduce the amount of code that is affected by each dsign decision.

2. **Cognitive load**: The amount of mental effort required to understand a piece of code. If a piece of code is hard to understand, it has high cognitive load. If it is easy to understand, it has low cognitive load. Good design minimizes cognitive load. There is a greater risk of risk of bugs in code with high cognitive load. Cognitive load arises in many ways, such as APIs with many methods, global variables, inconsistencies and dependencies.

3. Unknown unknowns: When you are working on a piece of code, there are often things you don't know about it. These unknowns can make it hard to understand the code and can lead to bugs. Good design minimizes unknown unknowns by making the code more self-explanatory and by providing clear documentation.

Of the three symotoms of complexity, unknown unknowns are the most dangerous because they can lead to unexpected behavior and bugs.

An obvious system is one where developers can easily see how to make a change without having to understand the entire system. An obvious system has low cognitive load and few unknown unknowns.

- **Causes of complexity**:

Complexity is caused by two things: dependencies and obscurity. Dependencies exist when a given piece of code cannot be understood and modified in isolation. Obscurity exists when a piece of code is hard to understand, obscurity comes about because of inadequate documentation. One of goal of software design is to reduce the number of dependencies and to make the code more obvious.

- **Strategic programming**:

First step towards becoming a good software designer is to realize that working code is not enough. You must also think about the design of the code. You must be willing to throw away working code if it is not well designed. You must be willing to refactor code to improve its design. You must be willing to spend time thinking about the design of your code before you start writing it. These investments will slow you down in the short term, but they will pay off in the long term.

When you discover a design problem, stop and think about how to fix it. Don't just hack a quick fix. Take the time to find a better design. This might mean refactoring existing code or it might mean redesigning the entire system.

- **Modularization**:

A software module is a piece of code that can be understood, developed, and tested in isolation. A module has a well-defined interface that specifies how it can be used by other modules. A module should have low complexity, so that it is easy to understand and modify. A module should also have few dependencies, so that it can be developed and tested in isolation.

The goal of modular design is to minimize the dependencies between modules. In order to manage dependencies, we think of each module in two parts: an interface and an implementation. The interface is the part of the module that is visible to other modules. The implementation is the part of the module that is hidden from other modules. By hiding the implementation, we can change it without affecting other modules.

**The best modules are those whose interfaces are much simpler than their implementations. Such modules has two advantages: First, a simple interface minimizes the complexity that a module imposes on the rest of the system. Second, a simple interface makes it easier to change the implementation without affecting other modules.**

The interface contains two kinds of information:

1. Formal information: The names and types of the methods and data that are visible to other modules.
2. Informal information: The documentation that explains how to use the module, i.e. if other modules should call the methods in a certain order, or if there are any preconditions or postconditions that must be satisfied etc.

For most interfaces, the informal information is more important than the formal information. A well-documented interface can be used effectively even if the formal information is complex. A poorly documented interface is hard to use even if the formal information is simple.

- **Abstraction**:

An abstraction is a simplified representation of a complex system. Abstractions are used to hide complexity and to make it easier to understand and work with complex systems. In software design, abstractions are used to create modules that can be understood and developed in isolation. An abstraction can go wrong in two ways.

1. First, it can include details that are not really important; when this happens, it makes the abstraction more complicated than necessary, which increases the cognitive load on developers using the abstraction.
2. The second error is when an abstraction omits details that really are important. This results in obscurity: developers looking only at the abstraction will not have all the information they need to use the abstraction correctly.

An abstraction that omits the important details is called a leaky abstraction. A leaky abstraction is one that does not completely hide the complexity of the underlying system. Leaky abstractions are dangerous because they can lead to bugs and unexpected behavior.

- **Deep Modules**:

Those modules that have a lot of implementation hidden behind a simple interface are called deep modules. Deep modules are desirable because they minimize the complexity that a module imposes on the rest of the system. Deep modules also make it easier to change the implementation without affecting other modules.

Module depth is a way of thinking about cost versus benefit. The cost of a module is the complexity that it imposes on the rest of the system. The benefit of a module is the amount of complexity that it hides behind its interface. A deep module has low cost and high benefit.

- **Shallow Modules**:

One whose interface is about as complex as its implementation is called a shallow module. Shallow modules are undesirable because they impose a lot of complexity on the rest of the system. Shallow modules also make it difficult to change the implementation without affecting other modules.

An example of shallow module

```code
private void addNullValueForAttribute(String attribute) {
  data.put(attribute, null);
}
```

Its a shallow module because it exposes a method that does very little beyond a direct delegation—it takes an attribute and simply puts a null value into a map:

- Low Abstraction: It does not hide or encapsulate any complex logic, invariant, or validation.
- Minimal Logic: The method does not check input, manage error cases (e.g., null attribute), or add business meaning; it just passes responsibility. There’s no defensive programming, error-handling, or additional intent .
- Thin Interface: The functionality provided is not richer than the underlying data structure (the map); anyone with access to the map could do the same operation, reducing the method’s modular value.

**A shallow module is a <font color="red">RED</font> Flag**

- **Classitis**

Unfortunately, the value of deep classes is not widely appreciated today. The conventional wisdom in programming is that classes should be small, not deep.
Students are often taught that the most important thing in class design is to break up larger classes into smaller ones. The same advice is often given about
methods: “Any method longer than N lines should be divided into multiple methods” (N can be as low as 10). This approach results in large numbers of
shallow classes and methods, which add to overall system complexity.

Classitis may result in classes that are individually simple, but it increases the complexity of the overall system. Small classes don’t contribute much functionality, so there have to be a lot of them, each with its own interface. These interfaces accumulate to create tremendous complexity at the system level. Small classes also result in a verbose programming style, due to the boilerplate required for each class.

- **Information Hiding**

Module should encapsulate a few pieces of knowledge, which represent design decisions. The knowledge is embedded in the module’s implementation but does
not appear in its interface, so it is not visible to other modules.

Information hiding reduces complexity in two ways.

1. First, it reduces the number of dependencies between modules, which makes it easier to understand and modify each module in isolation.
2. Second, it makes it easier to change the implementation of a module without affecting other modules.

- **Information Leakage**

It occurs when a design decision is reflected in multiple modules. When this happens, a change to the design decision requires changes to multiple modules, which increases complexity. If a piece of information is reflected in the interface for a module, then it is not hidden, and it is not information hiding.

One example is let's say there a file and two modules that read and write to it. If the file format changes, then both modules must be changed to accommodate the new format. This is an example of information leakage.

Information leakage is a <font color="red">RED</font> flag.

- **Temporal Decomposition**

In temporal decomposition, the structure of a system corresponds to the time order in which operations will occur. Consider an application that reads a file in a particular format, modifies the contents of the file, and then writes the file out again. With temporal decomposition, this application might be broken into three classes: one to read the file, another to perform the modifications, and a third to write out the new version. Both the file reading and file writing steps have knowledge about the file format, which results in information leakage. The solution is to combine the core mechanisms for reading and writing files into a single class.

Temporal decomposition is a <font color="red">RED</font> flag.

Its important to avoid exposing internal data structures in the interface of a module. When you do this, you are exposing implementation details that should be hidden. This creates dependencies between modules and increases complexity.

- **OverExposure**

If the API for a commonly used feature forces users to deal with unnecessary complexity, then the API is overexposed. An overexposed API increases cognitive load and can lead to bugs.

Overexposure is a <font color="red">RED</font> flag.
