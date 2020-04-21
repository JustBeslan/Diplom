unit uSpectr;


interface
uses Sysutils,graphics,extctrls,windows;

procedure GetSpectr(filename:string;var spectr:array of integer);
function calc_fxy(energ11,energ21:array of integer):real;

implementation

type arr=array[0..10000]of byte;
     sampl=array[0..1024]of real;
     samplr=array[0..1024]of real;
     comp=record re,im:real;end;

procedure FFTR(buf:array of comp);stdcall; external 'fftc.dll';


const k=0.5;

type pikrec=record
  pos:integer;
  lpc:integer;
  l:integer;
end;

var  left                         :array[0..200000]of smallint;
     buf                          :array[0..200000]of byte;


procedure savevsd(s:string;energ:array of integer);
var f:file;
    x:integer;
begin
     assignfile(f,s);
     rewrite(f,1);
     blockwrite(f,energ,sizeof(energ),x);
     closefile(f);
end;

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
var i:integer;
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

procedure Fft(source:sampl; length,step:integer;var result:sampl);forward;
procedure Fft(source:sampl; length,step:integer;var result:sampl);
var  f,t:integer;
begin
  for f:=1 to Length do
    begin
     Result[f]:=0.0;
     for t:=1 to Length do
        Result[f]:=Result[f]+ Source[t]*(-cos(PI*f*t/Length/2));
    end;
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

procedure GetSpectr(filename:string;var spectr:array of integer);

var step                        :integer;
   sImage                       :array[1..500,1..128]of smallint;
   x,y,n                     :integer;
   energ                        :array[0..128]of integer;
   bufc                         :array [0..512]of comp;
   f                            :file;
   chastota                     :sampl;
   l                            :integer;
   begin_crop,end_crop          :integer;
   max,min                      :integer;
   xout,dz                      :real;
   I                            :Integer;
   xx                           :integer;

begin
  assignfile(f,filename);
  reset(f,1);
  for n:=1 to 200000 do buf[n]:=0;
  for n:=1 to 200000 do left[n]:=0;
  seek(f,58);
  BlockRead(F, buf, filesize(f), x);
  end_crop:=x-100;
  closefile(f);
  for x:=1 to 128 do energ[x]:=0;
  x:=1;
  begin_crop:=200;
  max:=0;
  min:=255;

  {пропускаем нули}
  for l:=begin_crop to end_crop do if buf[l]<>0 then break;
  begin_crop:=l;
  for l:=begin_crop to end_crop do if buf[l]<min then min:=buf[l];
  for l:=begin_crop to end_crop do
       left[l]:=round((buf[l]+buf[l-1]+buf[l+1])/3)-128;

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


  for l:=begin_crop to end_crop do
   begin
    if left[l]>max then max:=left[l];
   end;

  step:=round((end_crop-begin_crop)/500);
 {и анализируем}
  for x:=1 to 500 do for y:=1 to 128 do
   begin
     sImage[x,y]:=0;
   end;
 step:=64;

  for y:=1 to 128 do  energ[y]:=0;

  //-=-=-=-=-=  Analize

  for x:=1 to 500 do
   begin

  if x*step+begin_crop< end_crop then begin

        for i:=0 to 511 do
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
     for y:=1 to 125 do
      begin
      l:=abs(round(chastota[y]));
      energ[y]:=energ[y]+l;
      if l>255 then l:=255;
      if l<0 then l:=0;
      end;
   end;
end;

//-=-=-=-=-=-=- end analize

     energ[126]:=0;

    for x:=1 to 125 do
    begin
      if energ[x]>y then y:=energ[x];
    end;
    y:=round(y/128);
     xx:=1;
    if y>0 then
      begin
        for xx:=1 to 128 do ;//spectr[xx]:=round(energ[xx]/y);
        for xx:=0 to 127 do spectr[xx]:=round(energ[xx+1]/y);
        for xx:=1 to 128 do energ[xx]:=round(energ[xx]/y);
      end;

     SaveVSD(ChangeFileExt(filename,'.vsd'),energ);
end;

end.
