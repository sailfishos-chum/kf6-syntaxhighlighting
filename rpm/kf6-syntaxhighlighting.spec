%global kf6_version 6.18.0
%global qt6_version 6.8.4

Name:    kf6-syntaxhighlighting
Version: 6.18.0
Release: 1%{?dist}
License: LGPLv2+ and MIT
Summary: Syntax highlighting engine for structured text and code
Url:     https://invent.kde.org/frameworks/syntax-highlighting
Source0: %{name}-%{version}.tar.xz

BuildRequires: gcc gcc-c++ cmake
BuildRequires: kf6-extra-cmake-modules >= %{kf6_version}
BuildRequires: kf6-rpm-macros

BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6LinguistTools)

BuildRequires: cmake(Qt6Quick)
BuildRequires: cmake(Qt6Gui)

BuildRequires: perl

%description
KSyntaxHighlighting is a syntax highlighting engine for Kate-based editors
and other applications. It provides QML bindings used by NeoChat to highlight
code blocks in messages.

%package devel
Summary: Development files for kf6-syntaxhighlighting
Requires: %{name} = %{version}-%{release}

%description devel
Headers and CMake config files for building against KSyntaxHighlighting.

%prep
%autosetup -n %{name}-%{version}/upstream

%build
export SBOX_MAPPING_LOGLEVEL=error
#export SBOX_QUIET=1
# Disable LTO
%global _lto_cflags %{nil}

%cmake_kf6 \
    -Wno-dev \
    -DKSYNTAXHIGHLIGHTING_USE_GUI=ON \
    -DQRC_SYNTAX=OFF \
    -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install

# let's own this
install -d %{buildroot}%{_kf6_datadir}/org.kde.syntax-highlighting/syntax

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSES/
%{_kf6_bindir}/*
%{_kf6_libdir}/libKF6SyntaxHighlighting.so.*
%{_kf6_qmldir}/org/kde/syntaxhighlighting/
%{_datadir}/locale/*/LC_MESSAGES/syntaxhighlighting6_qt.qm
%{_datadir}/qlogging-categories6/ksyntaxhighlighting.*
%{_kf6_datadir}/org.kde.syntax-highlighting/syntax-bundled/
%dir %{_kf6_datadir}/org.kde.syntax-highlighting/syntax

%files devel
%{_kf6_includedir}/KSyntaxHighlighting/
%{_kf6_libdir}/libKF6SyntaxHighlighting.so
%{_kf6_libdir}/cmake/KF6SyntaxHighlighting/
