## Overview

- Java's required that every object has identity, even if simple domain values don't want it, means worse performance. 
Typically, the JVM has to allocate memory for each newly created object, distinguishing it from every object already 
in the system, and reference that memory location whenever the object is used or stored. This causes the garbage 
collector to work harder, taking cycles away from the application.

- A value object is an object that does not have identity. A value object is an instance of a value class. Two value 
objects are the same according to == if they have the same field values, regardless of when or how they were created.

- Two variables of a value class type may hold references to different memory locations, but refer to the same value 
object—much like two variables of type int may hold the same int value.

### Programming without identity

- By opting out of identity, developers are opting in to a programming model that provides the best of both worlds: the 
abstraction of classes with the simplicity and performance benefits of primitives.


### Important points

- Classes with the value modifier are value classes; classes without the modifier are identity classes.

```java
value record Color(byte red, byte green, byte blue) {}
```

- Instance fields of value class are implicitly final.
- Instance method of value class must not be synchronized.
- A concrete value class is implicitly final and may have no subclasses.
- A abstract value class may have both value and identity subclasses.
- Identity classes may only be extended by identity classes.
- Interfaces may be extended by both identity and value classes.
- The class Object, which sits at the top of the class hierarchy, is considered an identity class and has identity 
instances, but in most respects behaves more like an interface and permits value subclasses.
- System.identityHashCode: The "identity hash code" of a value object is computed by combining the hash codes of the 
value object's fields. The default implementation of Object.hashCode continues to return the same value as identityHashCode.
- **Synchronization** -> Value objects do not have synchronization monitors. At compile time, the operand of a 
synchronized statement must not have a concrete value class type. At run time, if an attempt is made to synchronize on 
a value object (for example, where the operand of a synchronized statement has type Object), an IdentityException is 
thrown. Invocations of the wait and notify methods of Object will similarly fail at run time, because they require 
callers to first synchronize on the object's monitor.
- 