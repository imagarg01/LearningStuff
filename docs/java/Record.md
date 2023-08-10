## Journey in different JEPs
Record patterns were proposed as a preview feature by JEP 405 and delivered in JDK 19, and previewed a second time by 
JEP 432 and delivered in JDK 20. This feature has co-evolved with Pattern Matching for switch (JEP 441), with which it 
has considerable interaction. This JEP proposes to finalize the feature with further refinements based upon continued 
experience and feedback.

## Change of instanceof in different JEPs along with record

```java
//As of Java 16
record Point(int x, int y) {}

static void printSum(Object obj) {
    if (obj instanceof Point p) {
        int x = p.x();
        int y = p.y();
        System.out.println(x+y);
    }
}
```
Above in case 'obj' is of type class 'Point' it has been assigned to variable 'p' further accessor methods are getting 
called to extract the components.

It has been optimized with Java 21.
```java
static void printSum(Object obj) {
    if (obj instanceof Point(int x, int y)) {
        System.out.println(x+y);
    }
}
```

Above, a record disaggregates an instance of a record into its components.

## Nested Pattern with Record

```java
record Point(int x, int y) {}
enum Color { RED, GREEN, BLUE }
record ColoredPoint(Point p, Color c) {}
record Rectangle(ColoredPoint upperLeft, ColoredPoint lowerRight) {}


// As of Java 21
static void printXCoordOfUpperLeftPointWithPatterns(Rectangle r) {
    if (r instanceof Rectangle(ColoredPoint(Point(var x, var y), var c),
                               var lr)) {
        System.out.println("Upper-left corner: " + x);
    }
}
```

## Record with switch



## Important Points
- A record pattern can use var to match against a record component without stating the type of the component. In that 
case the compiler infers the type of the pattern variable introduced by the var pattern. For example, the pattern 
Point(var a, var b) is shorthand for the pattern Point(int a, int b).
- The canonical constructor, accessor methods, equals and hashCode can be overridden and thus customized.
- It is possible to add more constructors and arbitrary methods (but not fields or “private components” as this contradicts transparency).
- Records can implement interfaces.
- Record fields are final, but that doesn’t magically apply to what they reference, To prevent that, records should, if possible, create immutable copies of mutable data structures in their constructors.
 