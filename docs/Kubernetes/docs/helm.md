## Concepts

- A Chart is a Helm package. It contains all of the resource definitions necessary to run an application, tool, or
  service inside of a Kubernetes cluster.

- A Repository is the place where charts can be collected and shared.

- A Release is an instance of a chart running in a Kubernetes cluster. One chart can often be installed many times into
  the same cluster. And each time it is installed, a new release is created.

## File Structure

The directory name is the name of the chart (without versioning information).

1. Chart.yaml # A YAML file containing information about the chart
2. LICENSE # OPTIONAL: A plain text file containing the license for the chart
3. README.md # OPTIONAL: A human-readable README file
4. values.yaml # The default configuration values for this chart
5. values.schema.json # OPTIONAL: A JSON Schema for imposing a structure on the values.yaml file
6. charts/ # A directory containing any charts upon which this chart depends.
7. crds/ # Custom Resource Definitions
8. templates/ # A directory of templates that, when combined with values, will generate valid Kubernetes manifest files.
9. templates/NOTES.txt # OPTIONAL: A plain text file containing short usage notes

Helm reserves use of the charts/, crds/, and templates/ directories, and of the listed file names. Other files will be
left as they are.

## Useful Commands

- Search

```cmd
helm search repo << repo-name >>
```

you can find the names of the charts in repositories you have already added:

- Chart Management

| Command                                    | Description                                                                              |
| ------------------------------------------ | ---------------------------------------------------------------------------------------- | --- |
| helm create << name >>                     | # Creates a chart directory along with the common files and directories used in a chart. |
| helm package << chart-path >>              | # Packages a chart into a versioned chart archive file.                                  |     |
| helm lint << chart >>                      | # Run tests to examine a chart and identify possible issues:                             |
| helm show all << chart >>                  | # Inspect a chart and list its contents:                                                 |     |
| helm show values << chart >>               | # Displays the contents of the values.yaml file.                                         |
| helm pull << chart >>                      | # Download/pull chart.                                                                   |     |
| helm pull << chart >> --untar=true         | # If set to true, will untar the chart after downloading it.                             |
| helm pull << chart >> --verify             | # Verify the package before using it                                                     |     |
| helm pull << chart >> --version < number > | # Default-latest is used, specify a version constraint for the chart version to use.     |
| helm dependency list < chart >             | # Display a list of a chart’s dependencies:                                              |     |

- Install and UnInstall APPs

| Command                                                         | Description                                                                            |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------- | --- |
| helm install << name >> << chart >>                             | # Install the chart with a name                                                        |
| helm install << name >> << chart >> --namespace << namespace >> | # Install the chart in a specific namespace                                            |     |
| helm install << name >> << chart >> --set key1=val1,key2=val2   | # Set values on the command line (can specify multiple or separate values with commas) |
| helm install << name >> << chart> > --values <yaml-file/url>    | # Install the chart with your specified values.                                        |     |
| helm install << name >> << chart >> --dry-run --debug           | # Run a test installation to validate chart (p)                                        |
| helm install << name >> << chart >> --verify                    | # Verify the package before using it                                                   |     |
| helm install << name >> << chart >> --dependency-update         | # update dependencies if they are missing before installing the chart.                 |
| helm uninstall << name >>                                       | # Uninstall a release                                                                  |     |

- Important points while you are creating your own chart

1. There are two type of helm charts:

- Application Chart: This is the most common type of chart and is used to deploy an application. Its default chart type.
- Library Chart: This type of chart is used to create reusable templates that can be used in other charts.

2. In helm one chart can be depends on any number of charts. You can define the dependencies in the Chart.yaml file.
