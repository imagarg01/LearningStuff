## Overview

- It works on Windows, macOS, and Linux, and is designed to be fast and efficient. It is built on top of the Rust programming language, which makes it fast and secure. It is also extensible, so you can add your own commands and plugins to customize it to your needs.

- NuShell works on data, not just text. This means that you can use it to work with structured data like JSON, CSV, and XML, as well as text files. It also has built-in support for working with files, directories, and processes, so you can use it to automate tasks and build scripts.

- It follows unix philosophy of small, sharp tools that do one thing well. This means that you can combine commands together to build complex pipelines that do exactly what you need them to do. It also has a powerful scripting language that lets you write scripts to automate tasks and  build complex workflows.

- Every command in Nushell outputs data not text. This means that you can use the output of one command as the input to another command, and you can use the output of a command to create new data structures. This makes it easy to work with data in a flexible and powerful way.

- Data could be in any format, NuShell provides a way to convert data from one format to another. It also provides a way to filter data, sort data, and aggregate data. It also provides a way to create new data structures from existing data structures.

- Pros 

1. It makes shell interactive and user-friendly.
2. Works everywhere and easy to learn.
3. Error messages are clear and easy to understand.
4. Can be enhanced with plugins.

- Cons

1. Not Posix compliant.

## Few Examples

1. Print the current directory and filter the output based on different criteria.
```cmd
ls | where size > 100kb
```
It will print the files in the current directory whose size is greater than 100kb. In a nice tabular format.

2. Print the current directory and sort the output based on different criteria.
```cmd
ls | sort-by name --ignore-case
```
It will print the files in the current directory sorted by name in case-insensitive manner.

3. Let's not stop here, try to perform multiple operations in a single command.
```cmd
ls | sort-by size | reverse | first | get name
```
It will print the name of the largest file in the current directory.


```cmd
