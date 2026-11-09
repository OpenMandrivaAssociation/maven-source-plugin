Name:		maven-source-plugin
Version:	3.4.0
Release:	1
Summary:	Builds a JAR of project sources
Group:		Development/Java
License:	Apache-2.0
URL:		https://maven.apache.org/plugins/maven-source-plugin/
Source0:	https://github.com/apache/maven-source-plugin/archive/refs/tags/maven-source-plugin-%{version}.tar.gz#/maven-source-plugin-%{version}.tar.gz
# The tag has no license file. This copy is in git, so the build does not
# download it.
Source1:	LICENSE-2.0.txt
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	maven
BuildRequires:	maven-components >= 3.10.0
BuildRequires:	java-current-devel
# Generates META-INF/maven/plugin.xml. The separate annotations package
# conflicts with maven-components on the same index file.
BuildRequires:	maven-plugin-tools
BuildRequires:	mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:	mvn(org.apache.maven:maven-archiver)
BuildRequires:	maven-archiver >= 3.6.6
Requires:	maven-archiver >= 3.6.6
BuildRequires:	mvn(org.codehaus.plexus:plexus-archiver)
BuildRequires:	plexus-archiver >= 4.15.0
Requires:	plexus-archiver >= 4.15.0
BuildRequires:	mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:	plexus-utils >= 3.6.2
Requires:	plexus-utils >= 3.6.2
BuildRequires:	mvn(org.apache.maven:maven-model)
BuildRequires:	mvn(org.apache.maven:maven-plugin-api)
BuildRequires:	mvn(org.apache.maven:maven-artifact)
BuildRequires:	mvn(org.apache.maven:maven-core)
BuildRequires:	mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

Obsoletes:	maven2-plugin-source <= 0:2.0.8
Provides:	maven2-plugin-source = %{EVRD}
Obsoletes:	maven-source-plugin-javadoc < %{EVRD}

%description
Builds a JAR of the project's sources. Goals cover the main sources,
test sources, and generated test sources, with and without forking.
3.4.0 fails only when a different file is attached again. 4.0.0 is
still a beta, so this package stays on 3.4.0. Tests need JUnit
Jupiter, so they are not run.

%prep
%autosetup -n maven-source-plugin-maven-source-plugin-%{version}
rm -rf src/test src/it .github
cp -p %{SOURCE1} LICENSE
python - <<'PY'
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.apache.maven.plugins")
add(root, "artifactId", "maven-source-plugin")
add(root, "version", "%{version}")
add(root, "packaging", "maven-plugin")
add(root, "name", "Apache Maven Source Plugin")
props = ET.SubElement(root, tag("properties"))
add(props, "maven.compiler.release", "8")
add(props, "project.build.sourceEncoding", "UTF-8")
deps = ET.SubElement(root, tag("dependencies"))
items = (
    ("org.apache.maven", "maven-archiver", "3.6.6", None),
    ("org.codehaus.plexus", "plexus-archiver", "4.15.0", None),
    ("org.codehaus.plexus", "plexus-utils", "3.6.2", None),
    ("org.apache.maven", "maven-model", "3.10.0", "provided"),
    ("org.apache.maven", "maven-plugin-api", "3.10.0", "provided"),
    ("org.apache.maven", "maven-artifact", "3.10.0", "provided"),
    ("org.apache.maven", "maven-core", "3.10.0", "provided"),
    ("org.apache.maven.plugin-tools", "maven-plugin-annotations", "3.15.2", "provided"),
)
for group, artifact, version, scope in items:
    dep = ET.SubElement(deps, tag("dependency"))
    add(dep, "groupId", group)
    add(dep, "artifactId", artifact)
    add(dep, "version", version)
    if scope:
        add(dep, "scope", scope)
build = ET.SubElement(root, tag("build"))
plugins = ET.SubElement(build, tag("plugins"))
plugin = ET.SubElement(plugins, tag("plugin"))
add(plugin, "groupId", "org.apache.maven.plugins")
add(plugin, "artifactId", "maven-plugin-plugin")
# The lifecycle binding asks for 3.15.1. The packaged plugin is 3.16.0.
add(plugin, "version", "3.16.0")
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY

%files -f .mfiles
%doc LICENSE README.md
