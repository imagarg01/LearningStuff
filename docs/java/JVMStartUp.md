## Overview

Exact process followed at the time of JVM startup influenced by the type of application,
available resources, and the environment. The following steps are common in most of the cases:

1.  JNI_CreateJavaVM() is the entry point for creating a JVM instance. It is a native method
    that is implemented in the JVM. JNI_CreateJavaVM() is called by the application to create a JVM instance.

2.  **Loading of JVM**: The first step is to load the JVM. The JVM is loaded by the bootstrap
    class loader. The bootstrap class loader loads the core Java libraries located in
    the `jre/lib` directory.

## Reference

https://www.youtube.com/watch?v=ED1oc7gn5uY
