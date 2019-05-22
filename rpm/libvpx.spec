Name:           libvpx
Version:        1.7.0
Release:        1
Summary:        VPx codec library
License:        BSD
Group:          Applications/Multimedia
Url:            http://www.webmproject.org/
Source0:        %{name}-%{version}.tar.gz
Patch1:         0001-armv7-use-hard-float.patch
%ifarch %{ix86} x86_64
BuildRequires:  yasm
%endif

%description
WebM is an open, royalty-free, media file format designed for the web.

WebM defines the file container structure, video and audio formats.
WebM files consist of video streams compressed with the VPx video codecs
and audio streams compressed with the Vorbis audio codec.
The WebM file structure is based on the Matroska container.

%package devel
Summary:        VPx codec library - Development headers
License:        BSD-3-Clause and GPL-2.0+
Group:          Development/Languages/C and C++
Requires:       %{name} = %{version}

%description devel
Development headers and library

WebM is an open, royalty-free, media file format designed for the web.

WebM defines the file container structure, video and audio formats.
WebM files consist of video streams compressed with the VPx video codecs
and audio streams compressed with the Vorbis audio codec.
The WebM file structure is based on the Matroska container.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}

%description doc
%{summary}.

%prep
%setup -q -n %{name}-%{version}/upstream
%patch1 -p1

%build

./configure \
    --prefix=%{_prefix} --libdir=%{_libdir} \
    --disable-unit-tests --disable-examples --disable-docs \
    --enable-debug --enable-shared --disable-static \
    --enable-vp8 --enable-vp9 --enable-vp9-highbitdepth \
    --enable-multithread --enable-postproc \
    --enable-experimental --enable-spatial-svc \
%ifarch aarch64
    --disable-neon --disable-neon_asm \
%endif
%ifarch %{ix86} x86_64
    --as=yasm \
%endif
    --enable-pic --size-limit=8192x8192

make %{?_smp_mflags} verbose=yes GEN_EXAMPLES=

%install
%make_install verbose=yes GEN_EXAMPLES=

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version} \
        AUTHORS README CHANGELOG

%clean
rm -rf %{buildroot}

%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%files
%defattr(-, root, root)
%license LICENSE
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/vpx/
%{_libdir}/pkgconfig/vpx.pc
%{_libdir}/%{name}.so

%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}
