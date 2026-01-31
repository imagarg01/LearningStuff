## Overview

We used to create lots of classes to carry data also known as POJOs (Plain Old Java Object) or DTOs (Data Transfer Object).
Most of time Lombok has been used as choice of tool to generate getter/setters, constructors etc. Record come as good
replacement of Lombok whenever there is a need to create immutable data carrier class.

A record declaration specifies in header. JVM creats:

- equals, hashCode, and toString methods are created automatically.
- record's fields are final because the class is intended to serve as a simple "data carrier"

A simple record with two fields.

```java
record Rectangle(double width, double height) {}
```

## Feature of Record

- The canonical constructor, accessor methods, equals and hashCode can be overridden and thus customized.

- You can create generic record class, For example:

```java
record Triangle<C extends Coordinate> (C top, C left, C right) { }
```

- It is possible to add more constructors and arbitrary methods (but not fields or “private components” as this contradicts
  transparency).

- Records can implement interfaces.

- Record fields are final, but that doesn’t magically apply to what they reference, To prevent that, records should, if possible, create
  immutable copies of mutable data structures in their constructors.

- A record pattern can use var to match against a record component without stating the type of the component. In that
  case the compiler infers the type of the pattern variable introduced by the var pattern. For example, the pattern
  Point(var a, var b) is shorthand for the pattern Point(int a, int b).

- You can serialize and de-serialize the record classes, but you can't customize the process by providing writeObject,
  readObject, readObjectNoData, writeExternal or readExternal methods.

- Records can't inherit from a class because they already extend java.lang.Record implicitly.

### How instance filed work

For each component/field in the header, jdk will create

1. A private field name with the same name, in our example mentioned above; jdk will create

```java
private final double width;
private final double height;
```

1. It will also create public accessor for these field.

```java
Rectangle::width()
Rectangle::height()
```

1. Implementations of the equals and hashCode methods, which specify that two record classes are equal if they are of
   the same type and contain equal component values.

2. An implementation of the toString method that includes the string representation of all the record class's components
   , with their names.

### How constructor will work

- A canonical constructor will be created having same signature as the header.
- You can also override constructors

1. Example - **Declaring a public canonical constructor**

```java
public Rectangle(double height, double width) {
        if (height <= 0 || width <= 0) {
            throw new java.lang.IllegalArgumentException(
                String.format("Invalid values provided: %f, %f", height, width));
        }
        this.height = height;
        this.width = width;
    }
```

In above example we are simply validating the provided values in constructor.

1. Example - **Compact Constructor**

Use it, if you don't want to repeat signature in header and constructor

```java
record Rectangle(double height, double width) {
    public Rectangle {
        if (height <= 0 || width <= 0) {
            throw new java.lang.IllegalArgumentException(
                String.format("Invalid dimensions: %f, %f", height, width));
        }
    }
}
```

**Note** that the statements this.height = height; and this.width = width; which appear in the canonical constructor
do not appear in the compact constructor. At the end of a compact constructor, its implicit formal parameters are
assigned to the record class's private fields corresponding to its components.

### Writing your accessor method

JDK generate accessor method for each field present in header, you can declare your own accessor method as well provided
it follow the same characteristics. Here is a example

```java
record Rectangle(double height, double width) {

    // Public accessor method
    public double width() {
        System.out.println("Width is " + width);
        return width;
    }
}
```

Similarly we can implement other generated method as well like toString, hashcode and equals.

### You can declare static fields, static initializers and static methods, and they behave like in a normal class

```java
record Rectangle(double height, double width) {

    // Static field
    static double goldenRatio;

    // Static initializer
    static {
        goldenRatio = (1 + Math.sqrt(5)) / 2;
    }

    // Static method
    public static Rectangle createGoldenRectangle(double width) {
        return new Rectangle(width, width * goldenRatio);
    }
}
```

### You can declare instance method

```java
record Rectangle(double height, double width) {

    // Public instance method
    public Rectangle getRotatedRectangleBoundingBox(double angle) {
        RotationAngle ra = new RotationAngle(angle);
        double x = Math.abs(height * Math.cos(ra.angle())) +
                   Math.abs(width * Math.sin(ra.angle()));
        double y = Math.abs(height * Math.sin(ra.angle())) +
                   Math.abs(width * Math.cos(ra.angle()));
        return new Rectangle(x, y);
    }
}
```

### Change of instanceof in different JEPs along with record

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

### Nested Pattern with Record

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

### Record with switch

Record will work like any standard class with switch expression.

```java
record Point(int x, int y) {}

public class Main {
    public static void main(String[] args) {
        Point p = new Point(5, 6);
        String quadrant = switch (p) {
            case Point(int x, int y) when x > 0 && y > 0 -> "First Quadrant";
            case Point(int x, int y) when x < 0 && y > 0 -> "Second Quadrant";
            case Point(int x, int y) when x < 0 && y < 0 -> "Third Quadrant";
            case Point(int x, int y) when x > 0 && y < 0 -> "Fourth Quadrant";
            default -> "On an axis";
        };
        System.out.println(quadrant);
    }
}
```

### Record with Sealed classed and Interface

Combination of record and sealed classes can help us define data structures. Records are particularly useful for creating
simple data carriers, while sealed classes help in defining a closed set of subclasses or implementations for better
maintainability and security.

```java
public sealed interface Shape permits Circle, Square {
    
    // Records are implicitly final, so they cannot be abstract or non-sealed.
    // They are the "leaves" of the hierarchy.
    
    record Circle(double radius) implements Shape {}
    record Square(double side) implements Shape {}
}
```

### Serialization of Record classes

Records are serialized differently than other ordinary objects. Serialization process in more or less same as of a
ordinary object. During deserialization, if specified stream class is a record class, then

1. The stream fields are read and reconstructed to serve as the record's component values.
2. Record object is created by invoking the record's canonical constructor with the component values as arguments
   (or the default value for component's type if a component value is absent from the stream).
3. The process by which record objects are serialized or externalized cannot be customized; any implementation of
   writeObject, readObject, readObjectNoData, writeExternal, and readExternal methods defined by record classes are
   ignored during serialization and deserialization. However, a substitute object to be serialized or a designate
   replacement may be specified, by the writeReplace and readResolve methods, respectively.
4. The serialVersionUID of a record class is 0L unless explicitly declared. The requirement for matching serialVersionUID
   values is waived for record classes.

## Records in Spring Boot

Records are a game-changer for Spring Boot applications, primarily for **Data Transfer Objects (DTOs)** and **Read-Only Data**.

### 1. DTOs & JSON (Controller Layer)

Since Spring Boot 2.12+ (Jackson), Records are mapped automatically.

- **Request**: `@RequestBody UserRecord` works out of the box. Jackson uses the canonical constructor.
- **Response**: Records are serialized to JSON automatically.

```java
@RestController
public class UserController {
    // Automatic JSON -> Record mapping
    @PostMapping("/users")
    public CreateUserResponse create(@RequestBody CreateUserRequest req) {
        return new CreateUserResponse(req.username(), "CREATED");
    }
}
// Immutable DTOs! Match JSON exactly.
record CreateUserRequest(String username, String email) {}
record CreateUserResponse(String username, String status) {}
```

### 2. Database Projections (Repository Layer)

Spring Data JPA supports **Interface-based** and **Class-based** projections. Records are perfect for "Class-based Projections" (selecting specific columns) because they are immutable.

```java
// Entity
@Entity
class User { @Id Long id; String name; String email; String password; ... }

// Projection Record (Selects only Name and Email)
record UserSummary(String name, String email) {}

// Repository
interface UserRepository extends JpaRepository<User, Long> {
    // Spring Data effectively does: "SELECT name, email FROM User..."
    // and maps it to the Record constructor automatically.
    List<UserSummary> findByEmailEndingWith(String suffix);
}
```

### 3. Configuration Properties

Records are ideal for `@ConfigurationProperties` because config should be immutable once loaded.
*(Requires `@ConstructorBinding` or enabling record support in Spring Boot 2.6+)*

```java
@ConfigurationProperties(prefix = "app")
record AppConfig(String name, int timeout, String url) {}
```

### ⚠️ CRITICAL: Records as JPA Entities?

**DO NOT use Records as JPA `@Entity` classes.**

1. **Proxies**: Hibernate/JPA needs to create *proxies* (subclasses) for lazy loading. Records are `final`, so they cannot be proxied.
2. **Setters**: JPA relies on mutability (setters) to update state or separate creation from population. Records are immutable.
3. **No-Args Constructor**: JPA requires a no-args constructor. Records (canonical) typically enforce arguments.

> **Rule of Thumb**: Use **Classes** for Entities (DB State) and **Records** for DTOs/Projections (Data Movement).

## Performance & Internals

Do Records provide performance benefits? **Yes**, but often in subtle, architectural ways rather than raw CPU instructions.

### 1. Faster Reflection & Startup (Frameworks)

Traditional POJOs force frameworks (Jackson, Hibernate) to use "Dark Magic" (Reflection, `setAccessible(true)`, `Unsafe`) to force data into private fields.

- **Records**: Expose their API (Constructors/Accessors) publicly. Frameworks can simply **call the constructor**.
- **Benefit**: This is safer and often faster for libraries to bind data, potentially improving application startup time where thousands of DTOs are scanned and instantiated.

### 2. Smaller Bytecode (Disk/Memory Footprint)

A standard POJO with generated getters, setters, `equals`, `hashCode`, and `toString` contains a lot of bytecode instructions.

- **Records**: Use `invokedynamic`. The methods `equals`, `hashCode`, and `toString` do not have huge bodies in the bytecode. Instead, they point to a factory (`ObjectMethods.bootstrap`).
- **Benefit**: Smaller `.class` files and slightly less pressure on the ClassLoader.

### 3. Serialization Speed

Record serialization is designed to be **safe and fast**.

- **Traditional**: Uses magic to bypass constructors.
- **Records**: **ALWAYS** use the canonical constructor.
- **Benefit**: This simplifies the serialization graph and verification, making it more robust and potentially faster to reconstruct.

### 4. Future Proofing (Project Valhalla)

Records are compliant with "Value-Based Classes".

- **Future**: When Project Valhalla arrives, Records are the prime candidates to become **Value Types** (flat memory layout, no object header, incredibly fast CPU cache usage). Adopting records now prepares you for this free performance boost later.
