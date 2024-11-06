Name:           %{dz_repo}
Version:        %{dz_version} 
Release:        %{_vendor}%{?suse_version} 
Summary:        DevZone Projects Compiler 

Group:          Amusements/Games
License:        GPLv2
URL:            http://dev.openttdcoop.org

Source0:        %{name}-%{version}.tar

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildArch:      noarch

BuildRequires:  mercurial p7zip grfcodec unix2dos

%description
Build script for #openttdcoop DevZone projects

%prep
%setup -qn %{name}
rpm -qa | sort > rpmlist
 	
# update to the tag, if not revision
[ "$(echo %{version} | cut -b-1)" != "r" ] && hg up %{version}

%build
make bundle_zip ZIP="7za a" ZIP_FLAGS="-tzip -mx9" NFORENUM="nforenum" -j1 1>%{name}-%{version}-build.log 2>%{name}-%{version}-build.err.log
md5sum *.grf > %{name}-dev-%{version}.md5

%install

%check

%clean

%files

%changelog
