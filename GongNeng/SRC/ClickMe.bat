@echo off
echo ����ѡ���enter����������
echo ===================
choice /c 12 /M "��ѡ�����������ǻ�����1�������� 2�ǻ���"
if errorlevel 2 goto a
if errorlevel 1 goto b
:a
%~dp0%prog\huping.exe
goto end
:b
%~dp0%prog\ziping.exe
goto end