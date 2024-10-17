%{?_javapackages_macros:%_javapackages_macros}
Name:           maven-source-plugin
Version:        2.2.1
Release:        6.1%{?dist}
Summary:        Plugin creating source jar


License:        ASL 2.0
URL:            https://maven.apache.org/plugins/maven-source-plugin/
Source0:        http://repo1.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip

BuildArch: noarch

BuildRequires: maven-local
BuildRequires: java-devel >= 1:1.6.0
BuildRequires: plexus-utils
BuildRequires: ant
BuildRequires: maven-compiler-plugin
BuildRequires: maven-plugin-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: mvn(org.apache.maven.surefire:surefire-junit4)

Obsoletes: maven2-plugin-source < 0:%{version}-%{release}
Provides: maven2-plugin-source = 0:%{version}-%{release}

%description
The Maven 2 Source Plugin creates a JAR archive of the 
source files of the current project.

%package javadoc

Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.


%prep
%setup -q 
sed -i -e "s|plexus-container-default|plexus-container|g" pom.xml

%build
%mvn_file  : %{name}
%mvn_build -f

%install
%mvn_install


%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.2.1-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jan 16 2013 Michal Srb <msrb@redhat.com> - 2.2.1-3
- Build with xmvn

* Fri Nov 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-2
- Install license files
- Resolves: rhbz#876837

* Tue Oct 23 2012 Alexander Kurtakov <akurtako@redhat.com> 2.2.1-1
- Update to latest upstream release.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 8 2011 Alexander Kurtakov <akurtako@redhat.com> 2.1.2-6
- Use upstream source.
- Build with maven 3.x.
- Guidelines fixes.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 9 2010 Alexander Kurtakov <akurtako@redhat.com> 2.1.2-4
- Do not exclude plexus-container-default from dependencies.

* Fri May 28 2010 Alexander Kurtakov <akurtako@redhat.com> 2.1.2-3
- Add provides/obsoletes.

* Thu May 27 2010 Alexander Kurtakov <akurtako@redhat.com> 2.1.2-2
- Fix Url.
- More descriptive summary.
- Add missing BR.

* Thu May 27 2010 Alexander Kurtakov <akurtako@redhat.com> 2.1.2-1
- Initial package.
