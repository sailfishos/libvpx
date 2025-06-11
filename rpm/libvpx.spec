Name:           libvpx
Summary:        VP8/VP9 Video Codec SDK
Version:        1.15.2
Release:        1
License:        BSD
Url:            https://github.com/sailfishos/libvpx
Source0:        %{name}-%{version}.tar.bz2
Patch1:         0001-armv7-use-hard-float.patch
Patch2:         0002-Skip-diff-version-check-that-doesnt-work-with-busybo.patch
%ifarch %{ix86} x86_64
BuildRequires:  yasm
%endif

%description
libvpx provides the VP8/VP9 SDK, which allows you to integrate your applications
with the VP8 and VP9 video codecs, high quality, royalty free, open source codecs
deployed on millions of computers and devices worldwide.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}

%description devel
Development libraries and headers for developing software against
libvpx.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
./configure \
    --prefix=%{_prefix} --libdir=%{_libdir} \
    --disable-unit-tests --disable-examples --disable-tools --disable-docs \
    --enable-shared --disable-static \
    --enable-vp8 --enable-vp9 --enable-vp9-highbitdepth \
    --enable-multithread --enable-postproc --enable-vp9-postproc \
    --enable-experimental \
%ifarch %{ix86} x86_64
    --as=yasm \
%endif
%ifarch aarch64
    --disable-neon_i8mm \
%endif
    --enable-pic --size-limit=8192x8192

%make_build verbose=true

%install
%make_install verbose=true

%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/vpx/
%{_libdir}/pkgconfig/vpx.pc
%{_libdir}/%{name}.so
