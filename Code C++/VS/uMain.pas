unit uMain;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  Buttons, ExtCtrls, jpeg, StdCtrls, Db, ADODB, Grids, DBGrids, DBCtrls,comobj;

type
  TfoMain = class(TForm)
    SpeedButton1: TSpeedButton;
    SpeedButton2: TSpeedButton;
    SpeedButton3: TSpeedButton;
    SpeedButton4: TSpeedButton;
    SpeedButton5: TSpeedButton;
    SpeedButton6: TSpeedButton;
    SpeedButton7: TSpeedButton;
    ADOConnection1: TADOConnection;
    SpeedButton8: TSpeedButton;
    Image1: TImage;
    procedure SpeedButton4Click(Sender: TObject);
    procedure SpeedButton7Click(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure SpeedButton1Click(Sender: TObject);
    procedure SpeedButton2Click(Sender: TObject);
    procedure SpeedButton3Click(Sender: TObject);
    procedure SpeedButton8Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

  procedure RunSQL(q:TADOquery;close:boolean);

var
  foMain: TfoMain;
  ts:tstrings;
    apl_path:string;

implementation

uses uConfig, uNewUser, UCompare, USound, UAbout;

{$R *.DFM}
{
Procedure CreateMSAccessDatabase(filename : String);
var ÿDAO: Variant;
ÿ ÿ i:integer;
Const Engines:array[0..2] of string=('DAO.DBEngine.36', 'DAO.DBEngine.35', 'DAO.DBEngine');
ÿ ÿ Function CheckClass(OLEClassName:string):boolean;
ÿ ÿ var Res: HResult;
ÿ ÿ begin
ÿ ÿ ÿ Result:=CoCreateInstance(ProgIDToClassID(OLEClassName), nil, CLSCTX_INPROC_SERVER or CLSCTX_LOCAL_SERVER, IDispatch, Res)=S_OK;
ÿ ÿ end;
begin
ÿFor i:=0 to 2 do
ÿ ÿif CheckClass(Engines[i]) then
ÿ ÿ ÿbegin
ÿ ÿ ÿ ÿDAO := CreateOleObject(Engines[i]);
ÿ ÿ ÿ ÿDAO.Workspaces[0].CreateDatabase(filename, ';LANGID=0x0409;CP=1252;COUNTRY=0', 32);
ÿ ÿ ÿ ÿexit;
ÿ ÿ ÿend;
ÿRaise Exception.Create('DAO engine could not be initialized');
end;
}
procedure RunSQL(q:TADOquery;close:boolean);
begin
      try
        q.Open;
      except
        on EOleException do q.Active:=false;
        on EDatabaseError do q.Active:=false;
      end;
     if close then q.Active:=false;
 //    q.SQL.SaveToFile('db\1.sql');
end;

procedure TfoMain.SpeedButton4Click(Sender: TObject);
begin
  if not assigned(foconfig) then
   begin
    Application.CreateForm ( Tfoconfig, foconfig );
   end;
   foconfig.show;

end;

procedure TfoMain.SpeedButton7Click(Sender: TObject);
begin
  halt;
end;
procedure stringtobyte(s:string;var b:array of integer);
var x:integer;
begin
  for x:=0 to 127 do b[x]:=ord(s[x+1]);
end;
procedure TfoMain.FormCreate(Sender: TObject);
var        f:file;
  Energ1:array[1..128]of integer;
  Energ2,Energ3  : array[1..128]of byte;
  x:integer;
  v:array [0..127]of integer;
  s:string;
begin
  fomain.DoubleBuffered:=true;

end;

procedure TfoMain.SpeedButton1Click(Sender: TObject);
begin
  if not assigned(fonewuser) then
   begin
    Application.CreateForm ( Tfonewuser, fonewuser );
   end;
   fonewuser.show;

end;

procedure TfoMain.SpeedButton2Click(Sender: TObject);
begin
  if not assigned(form2) then
   begin
    Application.CreateForm ( Tform2, form2 );
   end;
   form2.show;
end;

procedure TfoMain.SpeedButton3Click(Sender: TObject);
begin
  if not assigned(analizeform) then
   begin
    Application.CreateForm ( Tanalizeform, analizeform );
   end;
   analizeform.show;
end;

procedure TfoMain.SpeedButton8Click(Sender: TObject);
begin
  if not assigned(fabout) then
   begin
    Application.CreateForm ( Tfabout, fabout );
   end;
   fabout.show;
end;

end.
