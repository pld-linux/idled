Summary:	Daemon that terminates users idle sessions
Summary(pl):	Demon który koñczy nieaktywne sesje u¿ytkowników
Name:		idled
Version:	1.16
Release:	2
Copyright:	non-profit
Group:		Daemons
Group(pl):	Serwery
Source0:	http://www.darkwing.com/idled/download/%{name}-%{version}.tar.gz
Source1:	idled.init
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-man.patch
Patch2:		%{name}-config.patch
Prereq:		fileutils
Prereq:		chkconfig
Requires:	mailx
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Idled is a daemon that runs on a machine to keep an eye on current
users. If users have been idle for too long, or have been logged on
for too long, it will warn them and log them out appropriately.

%description -l pl
Idled jest demonem który pilnuje aktualnie zalogowanych u¿ytkowników.
Je¶li u¿ytkownik by³ nieaktywny przez odpowiednio d³ugi czas, lub by³
za d³ugo zalogowany, idled ostrze¿e go i odpowiednio zakoñczy sesjê.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
make clean
make \
	OPTFLAGS="$RPM_OPT_FLAGS -DMAILMESSAGEFILE=\"%{_sysconfdir}/idled/logout.msg\""\
	LDFLAGS="-s" \
	DEST="%{_sbindir}" \
	CFDEST="%{_sysconfdir}/idled" \
	MDEST="%{_mandir}" \
	LOGDEST="/var/log"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/idled,%{_mandir}/man{5,8},/var/log,/etc/rc.d/init.d}
install idled $RPM_BUILD_ROOT%{_sbindir}
install idled.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5
install idled.8 $RPM_BUILD_ROOT%{_mandir}/man8
mv idled.cf.template idled.conf.template

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/idled

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	idled.conf.template README TODO CHANGES COPYRIGHT

touch $RPM_BUILD_ROOT/var/log/idled.log
touch $RPM_BUILD_ROOT%{_sysconfdir}/idled/logout.msg

%post
touch /var/log/idled.log
chmod 640 /var/log/cron
/sbin/chkconfig --add idled
if [ -f /var/lock/subsys/idled ]; then
	/etc/rc.d/init.d/idled restart >&2
else
	echo "Run \"/etc/rc.d/init.d/idled start\" to start idled."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/idled ]; then
		/etc/rc.d/init.d/idled stop >&2
	fi
	/sbin/chkconfig --del idled
fi

%files
%defattr(644,root,root,755)
%doc *.gz
%{_sysconfdir}/idled/logout.msg
%attr(755,root,root) %{_sbindir}/idled
%attr(754,root,root) /etc/rc.d/init.d/idled
%{_mandir}/man*/*
%attr(640,root,root) %ghost /var/log/idled.log
