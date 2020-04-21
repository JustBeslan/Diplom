unit USound;

interface

uses
  Windows,
  Messages,
  SysUtils,
  Classes,
  Graphics,
  Controls,
  Forms,
  Dialogs,
   StdCtrls, ExtCtrls,
  mmsystem, MPlayer, Menus, ComCtrls, Buttons, ImgList,math;

type
  TAnalizeForm = class(TForm)
    OpenDialog1: TOpenDialog;
    Label1: TLabel;
    MediaPlayer1: TMediaPlayer;
    ScrollBox1: TScrollBox;
    Image1: TImage;
    Image2: TImage;
    MainMenu1: TMainMenu;
    File1: TMenuItem;
    Open1: TMenuItem;
    Exit1: TMenuItem;
    About1: TMenuItem;
    Playcurrent1: TMenuItem;
    Data1: TMenuItem;
    Save1: TMenuItem;
    SaveDialog1: TSaveDialog;
    Label3: TLabel;
    Label4: TLabel;
    Compare1: TMenuItem;
    ProgressBar1: TProgressBar;
    Label6: TLabel;
    SpeedButton1: TSpeedButton;
    SpeedButton2: TSpeedButton;
    SpeedButton3: TSpeedButton;
    ImageList1: TImageList;
    MainForm: TMenuItem;
    Label7: TLabel;
    Label8: TLabel;
    Label9: TLabel;
    Label10: TLabel;
    Options1: TMenuItem;
    DeleteNoise1: TMenuItem;
    Image4: TImage;
    SpeedButton4: TSpeedButton;
    Image3: TImage;
    procedure FormCreate(Sender: TObject);
    procedure FormKeyPress(Sender: TObject; var Key: Char);
    procedure Exit1Click(Sender: TObject);
    procedure Open1Click(Sender: TObject);
    procedure Playcurrent1Click(Sender: TObject);
    procedure Save1Click(Sender: TObject);
    procedure Compare1Click(Sender: TObject);
    procedure About1Click(Sender: TObject);
    procedure SpeedButton1Click(Sender: TObject);
    procedure SpeedButton2Click(Sender: TObject);
    procedure SpeedButton3Click(Sender: TObject);
    procedure MainFormClick(Sender: TObject);
    procedure DeleteNoise1Click(Sender: TObject);
    procedure MediaPlayer1Notify(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  AnalizeForm: TAnalizeForm;

implementation

uses UCompare, UAbout, UCapture;

{$R *.DFM}
type arr=array[0..10000]of byte;
     sampl=array[0..1024]of real;
     samplr=array[0..1024]of real;
     comp=record re,im:real;end;
const k=0.5;

type pikrec=record
  pos:integer;
  lpc:integer;
  l:integer;
end;

//{$L fft.OBJ}

var step:integer=200;
    sImage:array[1..500,1..128]of smallint;
    piki:array[1..1000]of integer;
    pikAnalize:array[1..500]of pikrec;
    sImage2:array[1..500,1..128]of smallint;
    z,a,x,y,n,q,w:integer;
    energ:array[0..128]of integer;
    bufc:array [0..512]of comp;

procedure FFTR(buf:array of comp);stdcall; external 'fftc.dll';

function I0(X:real):real;
var Y, T, E, DE, SDE:real;
     i:integer;
begin
	Y := X/2;
	T := 0.0000000001;
        de:= 1;
	E :=DE;
	for i:=1 to 50 do
         begin
	  DE := de*Y / i;
          SDE := DE * DE;
          E := e+SDE;
          if (E*T-SDE>0) then break;
	end;
	result:= E;
end;

procedure KaiserWindow(source:sampl; length,b:integer;var result:sampl);
var i, k:integer;
   iI0b:real;
   h:real;
begin
  iI0b:=1.0 / I0(b);
  k := -(Length shr 2);
  for i:=1 to Length shr 2 do
   begin
    inc(k);
    h := I0(b*sqrt(1-sqr(2.0*k/(Length-1)))) * iI0b;
    source[i]:=source[i] *h;
    source[Length-1-i] := source[Length-1-i]*h;
   end;
   for i:=1 to length do result[i]:=source[i];
end;

procedure Liftering(source:sampl; length,b:integer;var result:sampl);
var i, k:integer;
   w,xout:real;
begin
  for i:=1 to Length do
   begin
      xout:=source[i]-0.9*w;
      w:=0.54-0.46*cos(2*pi*(i-6)/179);
      source[i]:=xout*w;
   end;
   for i:=1 to length do result[i]:=source[i];
end;

procedure ups(source:sampl; length:integer;var result:sampl);
var i:integer;
   w,xout,k,sq:real;
begin
  k:=0;
  for i:=1 to Length do if source[i]>k then k:=source[i];
  sq := 1.58 * sqrt(k);
  for i:=1 to length do result[i]:=round(source[i]*exp(sq/32));
end;


procedure Fft(source:sampl; length,step:integer;var result:sampl);forward;
procedure Fft(source:sampl; length,step:integer;var result:sampl);
var j,f:integer;
     t:integer;
begin
  for f:=1 to Length do
    begin
     Result[f]:=0.0;
     for t:=1 to Length do
        Result[f]:=Result[f]+ Source[t]*(-cos(PI*f*t/Length/2));
    end;
end;

procedure blur;forward;
procedure blur;

begin
  for x:=2 to 499 do for y:=2 to 127 do
   begin
     n:=0;
     for q:=-1 to 1 do for w:=-1 to 1 do n:=n+sImage[x+q,y+w];
     sImage2[x,y]:=round(n/9);
   end;
  for x:=1 to 500 do for y:=1 to 128 do
   begin
     sImage[x,y]:=sImage2[x,y];
   end;
end;

procedure savevsd(s:string);
var b:array[1..500*128]of byte;
    f:file;
begin
     for x:=1 to 500 do for y:=1 to 128 do b[(y-1)*500+x]:=sImage[x,y];
     assignfile(f,s);
     rewrite(f,1);
     blockwrite(f,energ,sizeof(energ),x);
     closefile(f);
end;

procedure readsound(s:string);
var
   pos:integer;
   f:file;
   left:array[0..300000]of smallint;
   buf:array[0..300000]of byte;
   chastota:sampl;
   chastotar:samplr;
   m,k:single;
   fh:hwnd;
   l,z,y:integer;
   begin_crop,end_crop,sLength:integer;
   pik,pikcheck,pikmax,piksum:real;
   pikneed{тот самый пик со словом}:boolean;
   pikcount,lPC,maxlpc,maxlPCpos:integer;
   max,min,n:integer;
   xout,dz:real;
   I,J:Integer;

label o1;
begin
  Analizeform.Image1.Canvas.Brush.Color:=clwhite;
  Analizeform.Image1.Canvas.Rectangle(0,0,Analizeform.Image1.width,Analizeform.Image1.Height);
  Analizeform.Image2.Canvas.Brush.Color:=clwhite;
  Analizeform.Image2.Canvas.Rectangle(0,0,Analizeform.Image2.width,Analizeform.Image2.Height);
  Analizeform.Image3.Canvas.Brush.Color:=clwhite;
  Analizeform.Image3.Canvas.Rectangle(0,0,Analizeform.Image3.width,Analizeform.Image3.Height);
  assignfile(f,s);
  reset(f,1);
  Analizeform.label1.caption:=s;
  y:=0;
  for n:=1 to 300000 do buf[n]:=0;
  for n:=1 to 300000 do left[n]:=0;
  seek(f,58);
  BlockRead(F, buf, filesize(f), x);
  analizeform.label9.Caption:=inttostr(x);//length
  end_crop:=x-100;
  closefile(f);
  Analizeform.image1.width:=500;
  Analizeform.image2.width:=500;
  fh:=Analizeform.image2.canvas.handle;
  for x:=1 to 128 do energ[x]:=0;
  x:=1;
  Analizeform.image1.Canvas.moveto(x,round(left[x*step]/3)+2);
  begin_crop:=200;
  slength:=0;
  max:=0;
  min:=255;

  {пропускаем нули}
  for l:=begin_crop to end_crop do if buf[l]<>0 then break;
  begin_crop:=l;
  for l:=begin_crop to end_crop do if buf[l]<min then min:=buf[l];
  for l:=begin_crop to end_crop do
       left[l]:=round((buf[l]+buf[l-1]+buf[l+1])/3)-128;

//  for l:=begin_crop to end_crop do left[l]:=buf[l]-128;

  for l:=begin_crop to end_crop do
    begin
       xout:=LEFT[l]-0.90*dz;
       dz:=left[l];
       LEFT[l]:=round(xout*(0.54-0.46*cos((l-6)*6.2832/179)));
    end;

  repeat
   inc(begin_crop);
  until abs(left[begin_crop]-left[begin_crop+1])>4;

  repeat
   dec(end_crop);
  until abs(left[end_crop]-left[end_crop-1])>4;
  begin_crop:=begin_crop+512;
  end_crop:=end_crop-512;

  analizeform.label7.Caption:='Begin '+inttostr(begin_crop);
  analizeform.label8.Caption:='end   '+inttostr(end_crop);

  for l:=begin_crop to end_crop do
   begin
    if left[l]>max then max:=left[l];
   end;

  step:=round((end_crop-begin_crop)/500);
  Analizeform.Label10.Caption:=inttostr(step);
 {и анализируем}
 Analizeform.DoubleBuffered:=true;
  for x:=1 to 500 do for y:=1 to 128 do
   begin
     sImage[x,y]:=0;
   end;
 step:=64;

  for y:=1 to 128 do  energ[y]:=0;

  //-=-=-=-=-=  Analize

  for x:=1 to 500 do
   begin
   { if x mod 20 = 0 then
     begin
       Analizeform.ProgressBar1.Position:= x div 5;
       application.ProcessMessages;
     end; }
    Analizeform.image1.Canvas.lineto(x,round(left[x*step+begin_crop]/3)+50);
//////////////////////
  if x*step+begin_crop< end_crop then begin

        for i:=0 to 512 do
         begin
         bufc[I].Re:= left[i+x*step+begin_crop];
         bufc[I].Im:=0;
         end;

  FFTR(bufc);//----

  for i:=128 to 256 do chastota[i-128]:=(sqrt(sqr(bufc[I].Im)+sqr(bufc[I].re)));

  Ups(chastota,128,chastota);
  Liftering(chastota,128,20,chastota);
  KaiserWindow(chastota,128,20,chastota);
//////////////////////
    pik:=0;
    pikmax:=0;
     for y:=1 to 125 do
      begin
      l:=abs(round(chastota[y]));
      energ[y]:=energ[y]+l;
      if l>255 then l:=255;
      if l<0 then l:=0;
      sImage[x,y]:=l;
      pik:=pik+l;
      end;
      pik:=pik/20;
      piksum:=piksum+pik;
      if pikmax<pik then pikmax:=pik;
   end;
end;

//-=-=-=-=-=-=- end analize

  x:=0;y:=0;
  fh:=Analizeform.image2.canvas.handle;
  for x:=1 to 500 do for y:=1 to 128 do
   begin
     l:=abs(sImage[x,y]);
     Windows.SetPixel(FH, X, y, rgb(l,l,l));
   end;
    Analizeform.Image2.Refresh;
    y:=0;
    n:=0;
    for x:=1 to 128 do n:=n+energ[x];
    n:=round(n/128);

   { for x:=1 to 1 do for y:=2 to 127 do
       energ[y]:=round((energ[y-1]+energ[y]+energ[y+1])/3);
    }
    //ищем пики в энергии
     energ[126]:=0;
    for x:=1 to 125 do
    begin
      if energ[x]>y then y:=energ[x];
    end;
    y:=round(y/128);

    x:=0;
    if y>0 then
      begin
        for x:=1 to 128 do energ[x]:=round(energ[x]/y);
        Analizeform.Image4.Canvas.MoveTo(0,128);
        for x:=1 to 128 do Analizeform.Image4.Canvas.LineTo(x,128-energ[x]);
      end;

  Analizeform.Image3.Canvas.MoveTo(0,0);
  Analizeform.Image3.Canvas.Brush.Color:=clblack;
//  Analizeform.Image3.Canvas.MoveTo(100,100);
  for x:=1 to 500 do
  begin
     m:=0;
     for y:=1 to 128 do
      begin
       m:=m+simage[x,y];
      end;
    Analizeform.Image3.Canvas.lineTo(x,round(m/256));
   end;

   SaveVSD(ChangeFileExt(s,'.vsd'));

end;

procedure TAnalizeForm.FormCreate(Sender: TObject);
begin
  Analizeform.Image4.Canvas.Brush.Color:=clwhite;
  Analizeform.Image4.Canvas.Rectangle(0,0,Analizeform.Image4.width,Analizeform.Image4.Height);
  Analizeform.Image4.Canvas.Brush.Color:=clblack;
 // readSound('sapr.wav');
end;

procedure TAnalizeForm.FormKeyPress(Sender: TObject; var Key: Char);
begin
halt;
end;

procedure TAnalizeForm.Exit1Click(Sender: TObject);
begin
 halt;
end;

procedure TAnalizeForm.Open1Click(Sender: TObject);
begin
  Analizeform.OpenDialog1.Execute;
  if Analizeform.OpenDialog1.FileName<>'' then readSound(Analizeform.OpenDialog1.FileName );
end;

procedure TAnalizeForm.Playcurrent1Click(Sender: TObject);
begin
   Analizeform.MediaPlayer1.FileName:=Analizeform.Label1.caption;
   Analizeform.MediaPlayer1.open;
   Analizeform.MediaPlayer1.play;
end;

procedure TAnalizeForm.Save1Click(Sender: TObject);

begin
  Analizeform.SaveDialog1.Execute;
  if Analizeform.SaveDialog1.FileName<>'' then
   begin
      savevsd(Analizeform.SaveDialog1.FileName);
   end;
end;

procedure TAnalizeForm.Compare1Click(Sender: TObject);
begin
 form2.showmodal;
end;

procedure TAnalizeForm.About1Click(Sender: TObject);
begin
  fAbout.showmodal;
end;

procedure TAnalizeForm.SpeedButton1Click(Sender: TObject);
begin
  Analizeform.OpenDialog1.Execute;
  if Analizeform.OpenDialog1.FileName<>'' then readSound(Analizeform.OpenDialog1.FileName );
end;

procedure TAnalizeForm.SpeedButton2Click(Sender: TObject);
begin
   Analizeform.SaveDialog1.Execute;
  if Analizeform.SaveDialog1.FileName<>'' then
   begin
      savevsd(Analizeform.SaveDialog1.FileName);
   end;
end;

procedure TAnalizeForm.SpeedButton3Click(Sender: TObject);
begin
  form2.showmodal;
end;

procedure TAnalizeForm.MainFormClick(Sender: TObject);
begin

  if not assigned(captureform) then
   begin
    Application.CreateForm ( Tcaptureform, captureform );
   end;
   captureform.show;

end;

procedure TAnalizeForm.DeleteNoise1Click(Sender: TObject);
begin
  analizeform.DeleteNoise1.Checked:=not analizeform.DeleteNoise1.Checked;
end;

procedure TAnalizeForm.MediaPlayer1Notify(Sender: TObject);
begin
 // label1.Caption:=inttostr(analizeform.MediaPlayer1.Position);

end;

end.

