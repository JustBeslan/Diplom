unit uNewUser;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls,  DXClass, DXSounds, extCtrls, Buttons,Wave,uSpectr,Registry,umain,
  Db, ADODB,comobj,UsersList, ImgList;

type
  TfoNewUser = class(TForm)
    Panel1: TPanel;
    Image1: TImage;
    Memo1: TMemo;
    Panel2: TPanel;
    SpeedButton7: TSpeedButton;
    Panel3: TPanel;
    Timer1: TTimer;
    Label1: TLabel;
    Label2: TLabel;
    Image2: TImage;
    Image3: TImage;
    Image4: TImage;
    Image5: TImage;
    Image6: TImage;
    Image7: TImage;
    CheckBox1: TCheckBox;
    Bevel1: TBevel;
    Label3: TLabel;
    Label4: TLabel;
    Label5: TLabel;
    Label6: TLabel;
    Edit1: TEdit;
    Label7: TLabel;
    Label8: TLabel;
    Label9: TLabel;
    Edit3: TEdit;
    SpeedButton1: TSpeedButton;
    Label10: TLabel;
    Label11: TLabel;
    ADOQuery1: TADOQuery;
    ADOTable1: TADOTable;
    edit2: TComboBox;
    ImageList1: TImageList;
    Image8: TImage;
    Image9: TImage;
    procedure SpeedButton7Click(Sender: TObject);
    procedure CheckBox1Click(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure FormCreate(Sender: TObject);
    procedure Image5MouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure Image5MouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure SpeedButton1Click(Sender: TObject);
  private
    FCapture: TSoundCaptureStream;
    FWaveStream: TWaveStream;
    procedure CaptureFilledBuffer(Sender: TObject);
  public
    { Public declarations }
  end;
type
     comp=record re,im:real;end;
var
  foNewUser             : TfoNewUser;
  Needformat,i,x,y      : integer;
  bufc                  : array [1..512]of comp;
  Energ1,Energ2,Energ3  : array[1..128]of integer;
  CurSampl              : integer=0;
  e1,e2,e3              : boolean;
    ts:tstrings;

procedure FFTR(buf:array of comp);stdcall; external 'fftc.dll';

implementation

{$R *.DFM}

function calc_fxy(energ11,energ21:array of integer):real;
var mx,my,s1,s2,s3:real;
    i:integer;
begin
    mx:=0;my:=0;
    for i:=0 to 127 do
     begin
       mx:=mx+energ11[i];
       my:=my+energ21[i];
     end;
    mx:=mx/128;
    my:=my/128;
    s1:=0;s2:=0;s3:=0;
    for i:=0 to 127 do s1:=s1+((energ11[i]-mx)*(energ21[i]-my));
    for i:=0 to 127 do s2:=s2+(sqr(energ11[i]-mx));
    for i:=0 to 127 do s3:=s3+(sqr(energ21[i]-my));
    s2:=sqrt(s2);
    s3:=sqrt(s3)*s2;
    if s3<>0 then result:=abs(s1/s3) else result:=0;
end;


procedure TfoNewUser.SpeedButton7Click(Sender: TObject);
begin
close;
end;

procedure TfoNewUser.CaptureFilledBuffer(Sender: TObject);
var buf:array[0..512]of byte;
    bufI:array[0..512]of integer;
    i,x,max:integer;
    Image:timage;
begin
  FWaveStream.CopyFrom(FCapture, FCapture.FilledSize);
  FWaveStream.Seek(FWaveStream.Size-512,0);
  FWaveStream.read(buf,512);

        for i:=1 to 512 do
         begin
         bufc[I].Re:= buf[i]-128;
         bufc[I].Im:=0//left[i+x*step+begin_crop];
         end;
    fftr(bufc);
  if cursampl=0 then image:=image1;
  if cursampl=1 then image:=image2;
  if cursampl=2 then image:=image3;
  if cursampl=3 then image:=image4;
  Image.Canvas.Brush.Color:=clwhite;
  Image.Canvas.Rectangle(0,0,Image.width,Image.Height);
   for i:=128 to 256 do bufi[i-128]:=round((sqrt(sqr(bufc[I].Im)+sqr(bufc[I].re)))/3);
   for i:=1 to 128 do if bufi[i]>255 then bufi[i]:=255;

    for x:=1 to 4 do for y:=2 to 127 do
       bufi[y]:=round((bufi[y-1]+bufi[y]+bufi[y+1])/3);

  Image.Canvas.Brush.Color:=clblack;
   for i:=1 to 16 do
    begin
        max:=0;
        if (i-1)*8+x<126 then
        for x:=1 to 8 do if bufi[(i-1)*8+x]>max then max:=bufi[(i-1)*8+x];
        Image.Canvas.Rectangle((i-1)*8,128,i*8-1,128-max);
    end;//
end;

procedure TfoNewUser.CheckBox1Click(Sender: TObject);
begin
   if fonewuser.CheckBox1.Checked=false then
    begin
     timer1.Enabled:=false;
     if FCapture<>nil then
     FCapture.Stop;
     FWaveStream.Free; FWaveStream := nil;
     deletefile('_tmp.wav');

    end;
   if fonewuser.CheckBox1.Checked=true then
   begin
    FCapture.Free;
    FCapture := TSoundCaptureStream.Create(nil);
    FWaveStream := TWaveFileStream.Create('_tmp.wav', fmCreate);
    with FCapture.SupportedFormats[8] do
    FWaveStream.SetPCMFormat(22050, 8, 1);
    FWaveStream.Open(True);

    FCapture.OnFilledBuffer := CaptureFilledBuffer;

    FCapture.CaptureFormat := 8;
    FCapture.Start;
    timer1.Enabled:=true;
   end;

end;

procedure TfoNewUser.FormClose(Sender: TObject; var Action: TCloseAction);
begin
     foNewUser.Release;
     foNewUser := nil;
end;

procedure TfoNewUser.FormCreate(Sender: TObject);
var   Reg: TRegistry;
      s:string;
begin
  Reg := TRegistry.Create;
  try
    Reg.RootKey := HKEY_CURRENT_USER;
    if Reg.OpenKey('\Software\Microsoft\Windows\CurrentVersion\Explorer', false)
    then s:=Reg.REadString('Logon User Name');
  finally
    Reg.CloseKey;
    Reg.Free;
    inherited;
  end;
  edit2.Text:=s;
  edit1.Text:=s;
  GetLocalUserList(edit2.Items);
  doublebuffered:=true;
  e1:=false;
  e2:=false;
  e3:=false;

end;

procedure TfoNewUser.Image5MouseDown(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
begin
  if sender = image5 then
    begin
     Image5.Picture.Bitmap:=Image8.Picture.Bitmap;
     cursampl:=1;
    end;
  if sender = image6 then
    begin
     Image6.Picture.Bitmap:=Image8.Picture.Bitmap;
     cursampl:=2;
    end;

  if sender = image7 then
    begin
     Image7.Picture.Bitmap:=Image8.Picture.Bitmap;
     cursampl:=3;
    end;

  if cursampl<>0 then begin
  deletefile('test'+inttostr(cursampl)+'.wav');
   if fonewuser.CheckBox1.Checked=true then
    begin
     timer1.Enabled:=false;
     fonewuser.CheckBox1.Checked:=false;
     if FCapture<>nil then
     FCapture.Stop;
     FWaveStream.Free; FWaveStream := nil;
     deletefile('_tmp.wav');
    end;

    //--------

    FCapture.Free;
    FCapture := TSoundCaptureStream.Create(nil);
    FWaveStream := TWaveFileStream.Create('test'+inttostr(cursampl)+'.wav', fmCreate);
    with FCapture.SupportedFormats[8] do
    FWaveStream.SetPCMFormat(22050, 8, 1);
    FWaveStream.Open(True);

    FCapture.OnFilledBuffer := CaptureFilledBuffer;

    FCapture.CaptureFormat := 8;
    FCapture.Start;
    timer1.Enabled:=true;
   end;
end;

procedure bytetostring(b:array of integer;var s:string);
begin
  s:='';
  for x:=0 to 127 do
  s:=s+chr(b[x]+1);
end;

procedure stringtobyte(s:string;var b:array of integer);
begin
  for x:=0 to 127 do b[x]:=ord(s[x+1]);
end;

procedure TfoNewUser.Image5MouseUp(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);

var spectr:array[1..128]of integer;
    i1,i2,i3,max:real;
    i:integer;
    image:timage;
       f:file;
    s:string;
begin
  if FCapture<>nil then
  FCapture.Stop;
  FWaveStream.Free; FWaveStream := nil;

  if cursampl=1 then
    begin
      image:=image2;
      e1:=true;
      Image5.Picture.Bitmap:=Image9.Picture.Bitmap;
    end;
  if cursampl=2 then
    begin
      image:=image3;
      e2:=true;
      Image6.Picture.Bitmap:=Image9.Picture.Bitmap;
    end;
  if cursampl=3 then
    begin
      image:=image4;
      e3:=true;
      Image7.Picture.Bitmap:=Image9.Picture.Bitmap;
    end;

  getspectr('test'+inttostr(cursampl)+'.wav',spectr);

  Image.Canvas.Brush.Color:=clwhite;
  Image.Canvas.Rectangle(0,0,Image.width,Image.Height);
  Image.Canvas.MoveTo(0,128);
  for i:=1 to 128 do
   begin
    Image.Canvas.LineTo(i,128-spectr[i]);
    case cursampl of
     1:energ1[i]:=spectr[i];
     2:energ2[i]:=spectr[i];
     3:energ3[i]:=spectr[i];
     end;
   end;
    case cursampl of
     1:  begin
            assignfile(f,'test1.vsd');
            reset(f,1);
            blockread(f,energ1,512,x);
            closefile(f);
         end;
     2:  begin
            assignfile(f,'test2.vsd');
            reset(f,1);
            blockread(f,energ2,512,x);
            closefile(f);
         end;
     3:  begin
            assignfile(f,'test3.vsd');
            reset(f,1);
            blockread(f,energ3,512,x);
            closefile(f);
         end;
     end;
  timer1.Enabled:=false;
  cursampl:=0;

  if e1 and e2 and e3 then
   begin
     max:=0;
     i1:=calc_fxy(energ1,energ2);
     if i1>max then max:=i1;
     i2:=calc_fxy(energ2,energ3);
     if i2>max then max:=i2;
     i3:=calc_fxy(energ1,energ3);
     if i3>max then max:=i3;
     label9.caption:=inttostr(round(max*100));
     edit3.Text:=inttostr(round((i1+i2+i3)/0.03));
     label10.Caption:='1<>2 '+inttostr(round(i1*100))+'% 2<>3 '+inttostr(round(i2*100))+'% 1<>3 '+inttostr(round(i3*100))+'%';
   end;

end;

procedure TfoNewUser.SpeedButton1Click(Sender: TObject);
var name,login,s:string;
    x:integer;
    p:tblobfield;
       f:file;
    energ:array [0..127]of byte;
    us_id:integer;
begin
   if e1 and e2 and e3 then
   begin
      login:=edit2.text;
      name:=edit1.Text;
      ADOquery1.Active:=false;
      ADOquery1.SQL.Clear;
      ADOquery1.SQL.add('select * from userinfo where (deleted=0) and (login='+chr(39)+login+chr(39)+')');
      RunSQL(ADOquery1,false);
      us_id:=ADOquery1.FieldByName('user_id').asinteger;

      ADOquery1.Active:=false;
      ADOquery1.SQL.Clear;
      ADOquery1.SQL.add('delete from reg where user_id='+inttostr(us_id));
      RunSQL(ADOquery1,true);

      ADOquery1.Active:=false;
      ADOquery1.SQL.Clear;
      ADOquery1.SQL.add('delete from userinfo where login='+chr(39)+login+chr(39));
      RunSQL(ADOquery1,true);

      ADOquery1.SQL.Clear;
      ADOquery1.SQL.add('insert into userinfo(login,name)  values ('+chr(39)+login+chr(39)+','+chr(39)+name+chr(39)+')');
      RunSQL(ADOquery1,true);

      ADOquery1.SQL.Clear;
      ADOquery1.SQL.add('select * from userinfo where (deleted=0) and (login='+chr(39)+login+chr(39)+')');
      RunSQL(ADOquery1,false);
      us_id:=ADOquery1.FieldByName('user_id').asinteger;

      assignfile(f,'test1.vsd');
      reset(f,1);
      blockread(f,energ1,512,x);
      closefile(f);
      Bytetostring(energ1,s);
      ADOTable1.Insert;
      ADOTable1.FieldByName('user_id').asinteger:=us_id;
      ADOTable1.FieldByName('number').asinteger:=1;
      ADOTable1.FieldByName('spectr').asstring:=s;
      ADOTable1.Post;

      assignfile(f,'test2.vsd');
      reset(f,1);
      blockread(f,energ2,512,x);
      closefile(f);
      Bytetostring(energ2,s);
      ADOTable1.Insert;
      ADOTable1.FieldByName('user_id').asinteger:=us_id;
      ADOTable1.FieldByName('number').asinteger:=2;
      ADOTable1.FieldByName('spectr').asstring:=s;
      ADOTable1.Post;

      assignfile(f,'test3.vsd');
      reset(f,1);
      blockread(f,energ3,512,x);
      closefile(f);
      Bytetostring(energ3,s);
      ADOTable1.Insert;
      ADOTable1.FieldByName('user_id').asinteger:=us_id;
      ADOTable1.FieldByName('number').asinteger:=3;
      ADOTable1.FieldByName('spectr').asstring:=s;
      ADOTable1.Post;

      ShowMessage('Пользователь '+login+' добавлен');
   end;
end;

end.
