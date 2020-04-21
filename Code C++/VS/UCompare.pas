unit UCompare;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, Buttons, ExtCtrls, uNeurons;

type
  TForm2 = class(TForm)
    Image1: TImage;
    Image2: TImage;
    BitBtn1: TBitBtn;
    Button1: TButton;
    Button2: TButton;
    OpenDialog1: TOpenDialog;
    Label1: TLabel;
    Label2: TLabel;
    Label3: TLabel;
    Label4: TLabel;
    Label5: TLabel;
    Label6: TLabel;
    Button3: TButton;
    Label7: TLabel;
    Timer1: TTimer;
    BitBtn2: TBitBtn;
    Memo1: TMemo;
    BitBtn3: TBitBtn;
    Label8: TLabel;
    procedure BitBtn1Click(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure Button3Click(Sender: TObject);
    procedure Timer1Timer(Sender: TObject);
    procedure BitBtn2Click(Sender: TObject);
    procedure BitBtn3Click(Sender: TObject);
    procedure Button1Click(Sender: TObject);
    procedure Button2Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

const aks=1.5;

type koh = record
  inW:array[1..128] of real;
  s:real;
end;

var
  Form2: TForm2;


implementation
var
  koef:array[1..128]of real;
  energ:array[1..128]of real;
  energ1:array[1..128]of integer;
  energ2:array[1..128]of integer;
  koh_s:array[1..128] of koh;
  s,_y:real;
  fh:hwnd;
  a:real;
  tik,ener:integer;
  f:file;
    n,x,y,z,k,o:integer;
   {$R *.DFM}


function calc_fxy:real;
var mx,my,s1,s2,s3:real;
    i:integer;
begin
    mx:=0;my:=0;
    for i:=0 to 127 do
     begin
       mx:=mx+energ1[i];
       my:=my+energ2[i];
     end;
    mx:=mx/128;
    my:=my/128;
    s1:=0;s2:=0;s3:=0;
    for i:=0 to 127 do s1:=s1+((energ1[i]-mx)*(energ2[i]-my));
    for i:=0 to 127 do s2:=s2+(sqr(energ1[i]-mx));
    for i:=0 to 127 do s3:=s3+(sqr(energ2[i]-my));
    s2:=sqrt(s2);
    s3:=sqrt(s3)*s2;
    if s3<>0 then result:=abs(s1/s3) else result:=0;
end;

procedure TForm2.BitBtn1Click(Sender: TObject);
begin
  FORM2.CLOSE;
end;

procedure TForm2.FormCreate(Sender: TObject);
begin

 form2.Image1.Canvas.Brush.Color:=clwhite;
 form2.Image1.Canvas.Rectangle(0,0,form2.Image1.width,form2.Image1.Height);
 form2.Image2.Canvas.Brush.Color:=clwhite;
 form2.Image2.Canvas.Rectangle(0,0,form2.Image2.width,form2.Image2.Height);

end;

procedure TForm2.Button3Click(Sender: TObject);
begin
label8.Caption:=inttostr(round(calc_fxy*100));
end;

procedure TForm2.Timer1Timer(Sender: TObject);
begin
//    Net_Next;
end;


procedure TForm2.BitBtn2Click(Sender: TObject);

begin
      form2.DoubleBuffered:=true;
      assignfile(f,'v3_1.vsd');
      reset(f,1);
      blockread(f,energ1,512,x);
      closefile(f);
      s:=0;_y:=0;
      a:=0.04;


      for y:=1 to 128 do energ[y]:=energ1[y]/128;

      {нормализуем вектор}
      for y:=1 to 128 do s:=s+sqr(energ[y]);
      s:=sqrt(s);
      for y:=1 to 128 do energ[y]:=energ[y]/s;
      s:=0;

      {зададим коэфф кохонена}
      randomize;
      for x:=1 to 128 do
        begin
          for y:=1 to 128 do koh_s[x].inW[y]:=(random(100)-49)/50;
        end;

      for y:=1 to 128 do koef[y]:=0;
      x:=0;
      repeat
          inc(x);
          _y:=0;

          for z:=1 to 128 do
          begin
            s:=0;
            for y:=1 to 128 do s:=s+koh_s[z].inw[y]*energ[y];
            if s>_y then
             begin
              n:=z; {n - победивший нейрон}
              _y:=s;
             end;
          end;
          for y:=1 to 128 do koh_s[n].inw[y]:=koh_s[n].inw[y]+a*(energ[y]-koh_s[n].inw[y]);
          k:=n-round(32/(x/70+1)); if k<1 then k:=1;
          o:=n+round(32/(x/70+1)); if o>128 then o:=1;
          for z:=k to o do for y:=1 to 128 do
            koh_s[z].inw[y]:=koh_s[z].inw[y]+a*(energ[y]-koh_s[z].inw[y]); 

          s:=0;
          for y:=1 to 128 do s:=s+koh_s[n].inw[y]*energ[y];
          if x mod 10 = 0 then
           begin
{            a:=a-0.001;
            if a<0.005 then a:=0.005;}
            label7.Caption:=inttostr(x)+' : '+floattostr(s)+' : '+floattostr(sigmoid(s,aks));
            z:=form2.image2.canvas.handle;
            for k:=1 to 128 do for o:=1 to 128 do
            Windows.SetPixel(z, k, o, rgb(abs(round(koh_s[k].inw[o]*255)),0,0));
            form2.image2.Repaint;
            application.ProcessMessages;
           end;
         // sleep(3);
       until round(s*10000000000)=10000000000;
       memo1.Lines.Clear;
       for y:=1 to 128 do  memo1.lines.add({inttostr(y)+' : '+inttostr(energ1[y])+' : '+}floattostr(koh_s[n].inw[y]));


       z:=form2.image2.canvas.handle;
       for y:=1 to 128 do for x:=1 to 128 do
         Windows.SetPixel(z, X, y, rgb(abs(round(koh_s[y].inw[x]*255)),0,0));
         form2.image2.Repaint;
end;

procedure TForm2.BitBtn3Click(Sender: TObject);
begin
   form2.OpenDialog1.Execute;
   if form2.OpenDialog1.FileName<>'' then
     begin
      assignfile(f,form2.OpenDialog1.FileName);
      reset(f,1);
      blockread(f,energ1,512,x);
      closefile(f);
      s:=0;
      for y:=1 to 128 do energ[y]:=energ1[y]/128;
      for y:=1 to 128 do s:=s+sqr(energ[y]);
      s:=sqrt(s);
      for y:=1 to 128 do energ[y]:=energ[y]/s;
      s:=0;
      for y:=1 to 128 do s:=s+koh_s[n].inw[y]*energ[y];
      label3.Caption:=floattostr(s)+' : '+floattostr(sigmoid(s,aks))
                      +' : '+floattostr(sigmoid(s,aks)/sigmoid(1,aks));
     end;
end;

procedure TForm2.Button1Click(Sender: TObject);
begin
   form2.OpenDialog1.Execute;
   if form2.OpenDialog1.FileName<>'' then
     begin
      assignfile(f,form2.OpenDialog1.FileName);
      reset(f,1);
      blockread(f,energ1,512,x);
      closefile(f);
      label1.Caption:=form2.OpenDialog1.FileName;
     end;
end;

procedure TForm2.Button2Click(Sender: TObject);
begin
   form2.OpenDialog1.Execute;
   if form2.OpenDialog1.FileName<>'' then
     begin
      assignfile(f,form2.OpenDialog1.FileName);
      reset(f,1);
      blockread(f,energ2,512,x);
      closefile(f);
      label2.Caption:=form2.OpenDialog1.FileName;
     end;

end;

end.
