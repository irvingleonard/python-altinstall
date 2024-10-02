# Fedora Core 40 and compatibles

## Building RPMs

There are pre-built packages in the releases section of this project. The instructions assume that the working directory is the one containing this file.

In order to build the package you need to have a working [docker](https://www.docker.com/) environment and "prepare" the building container:

`docker build -t python-altinstall:fc40 .`

Then, to build the latest version:

`docker run --rm --volume "$PWD"/releases:/root/rpmbuild/SRPMS --volume "$PWD"/releases:/root/rpmbuild/RPMS python-altinstall:fc40 python310-altinstall.spec`

The resulting RPMs (including source RPMs) should land in the `releases` directory. There might be some issues with permissions, so you might want to run:

```sudo chown -R `whoami` releases/*```

## Updating SPECs

Since the last parameter to the "docker run" is the name of the SPEC file one might assume that is "passing" it to the container, which is not true. Instead, that parameter is the name used to identify the file that was copied over during the "docker build" phase. That's why you need to re-build the image every time you update the SPEC files, since running the existing image will only process the old version (or fail altogether, if it's a new SPEC file).
