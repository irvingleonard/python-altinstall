FROM mageia:9

RUN zypper --non-interactive update
RUN zypper --non-interactive install rpmdevtools rpmbuild

WORKDIR /root
RUN rpmdev-setuptree
VOLUME ["/root/rpmbuild/SRPMS", "/root/rpmbuild/RPMS"]

WORKDIR /root/rpmbuild/SPECS/
COPY *.spec .

RUN for spec_file in *.spec; do zypper --non-interactive install $(rpmspec -P $spec_file | grep BuildRequires | cut -f2 | xargs); done
RUN for spec_file in *.spec; do rpmdev-spectool -g -R $spec_file; done

ENTRYPOINT ["rpmbuild", "-ba"]
