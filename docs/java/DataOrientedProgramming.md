 q## OOP (Everything is an Object) 
The most direct way to implement it is to create classes that combine mutable state with the methods that operate on 
them. These classes usually encapsulate their state and often inherit the contract for their methods from interfaces 
that represent the common features of different classes in one type.

## Data Oriented Programming
- Model data immutably and transparently.
- Model the data, the whole data, and nothing but the data.
- Make illegal states unrepresentable.
- Separate operations from data.

1. An object is transparent if its internal state is accessible and constructable via the API, i.e.
 - There must be an access method for each field that returns the same (==) or at least an equal (equals) value.
 - There must be a constructor that accepts a value for all fields and, if they are in the valid range, saves them directly or at least as a copy.

2.