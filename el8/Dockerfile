FROM oraclelinux:8

RUN dnf -y upgrade
RUN dnf -y install rpmdevtools

WORKDIR /root
RUN rpmdev-setuptree
VOLUME ["/root/rpmbuild/SRPMS", "/root/rpmbuild/RPMS"]

WORKDIR /root/rpmbuild/SPECS/
COPY *.spec ./

RUN for spec_file in *.spec; do dnf builddep --enablerepo ol8_codeready_builder -y "$spec_file"; done
RUN for spec_file in *.spec; do spectool -g -R "$spec_file"; done
COPY *.patch /root/rpmbuild/SOURCES/

ENTRYPOINT ["rpmbuild", "-ba"]
