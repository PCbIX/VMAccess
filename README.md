# VMAccess

VMAccess stands for Virtual Machine Access, a small client-server RBAC utility for Hyper-V (Windows Server and Windows & Linux client machines supported).

## Getting Started

VMAccess is extremely easy to use, but you'll need somewhat 30 minutes to fully understand the requirements for the most reliable system configuration.
Don't worry, there's nothing sophisticated about it; you just need to read this manual carefully, **'Prerequisites'** and **'Installation'** sections, actually.

### Prerequisites

If you're going to simply utilize this tool, you can skip straight to **'Installing'**

To launch client and server applications there are no special requirements - all (Python interpreter + libraries + source code) files are already included.

If you want to further develop VMAccess, you'll need to install:

- Python 3.6 or newer (though earlier versions of Python, starting from Python 3.4, will probably be fine, too);
- 'portalocker' is used to guarantee that changes to log file would not be missed because of someone looking through log at the same time; get it by running 'pip install portalocker' in your terminal; look [(here)] (https://pypi.python.org/pypi/portalocker) for more details on 'portalocker';
- 'cx_Freeze' is used to build the executables out of source files; more details on cx_Freeze [here] (https://anthony-tuininga.github.io/cx_Freeze/).

Additionally, we recommend to use either PyCharm ([Community Edition] (https://anthony-tuininga.github.io/cx_Freeze/) is fine) or [VSCode] (https://code.visualstudio.com/Download) for development, though this advice is one big IMHO and is ridiculous in case you already have a Python IDE you're comfortable with.

### Installing



```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc