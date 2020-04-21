program UserReg;

uses
  Forms,
  sysutils,
  windows,
  inifiles,
  dialogs,
  Messages,
  Classes,
  Graphics,
  Controls,
  ExtCtrls,
  Menus,
  USound in 'USound.pas' {testing fft - AnalizeForm},
  UCompare in 'UCompare.pas' {testing neurons},
  UAbout in 'UAbout.pas' {fAbout},
  UCapture in 'UCapture.pas' {CaptureForm},
  uSpectr in 'uSpectr.pas',
  uMain in 'uMain.pas' {foMain},
  uConfig in 'uConfig.pas' {foConfig},
  uNewUser in 'uNewUser.pas' {foNewUser},
  Uneurons in 'Uneurons.pas';

{$R *.RES}

var x:integer;
    s:string;
begin
  Application.Initialize;
  apl_path:=getcurrentdir+'\';
  Application.CreateForm(TfoMain, foMain);
  Application.Run;
end.
