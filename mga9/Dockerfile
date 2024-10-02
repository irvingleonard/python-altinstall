FROM mageia:9

RUN urpmi --auto --auto-update
RUN urpmi --auto rpmdevtools

WORKDIR /root
RUN rpmdev-setuptree
VOLUME ["/root/rpmbuild/SRPMS", "/root/rpmbuild/RPMS"]

WORKDIR /root/rpmbuild/SPECS/
COPY *.spec .

RUN for spec_file in *.spec; do urpmi --auto $(rpmspec -P $spec_file | grep BuildRequires | cut -f2 | xargs); done
RUN for spec_file in *.spec; do rpmdev-spectool -g -R $spec_file; done

ENTRYPOINT ["rpmbuild", "-ba"]
