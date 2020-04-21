unit uInMain;


interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls,  DXClass, DXSounds, extCtrls, Buttons,Wave,uSpectr,
  uSpectrImage,Registry,
  jpeg, DB, ADODB,  Menus,
  comobj,opengl,bmp, cPanel;

type
  TfoInMain = class(TForm)
    Panel2: TPanel;
    SpeedButton7: TSpeedButton;
    Panel3: TPanel;
    Label1: TLabel;
    Label2: TLabel;
    Image2: TImage;
    Image5: TImage;
    Edit2: TEdit;
    Label7: TLabel;
    Label9: TLabel;
    Panel1: TPanel;
    Image1: TImage;
    Label3: TLabel;
    Label4: TLabel;
    Label5: TLabel;
    Label6: TLabel;
    ADOConnection1: TADOConnection;
    ADOQuery1: TADOQuery;
    Edit1: TEdit;
    Image3: TImage;
    Timer1: TTimer;
    procedure SpeedButton7Click(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure FormCreate(Sender: TObject);
    procedure Image5MouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure Image5MouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure SpeedButton7MouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure Timer1Timer(Sender: TObject);
  private
    FCapture: TSoundCaptureStream;
    FWaveStream: TWaveStream;
    procedure CaptureFilledBuffer(Sender: TObject);
  public
    { Public declarations }
  end;
type
     comp=record re,im:real;end;

const
  GridSize = 31;

type TGLCoord = Record
       X, Y, Z : glFloat;
     end;

var
  h_Wnd  : HWND;                     // Global window handle
  h_DC   : HDC;                      // Global device context
  h_RC   : HGLRC;                    // OpenGL rendering context
  keys : Array[0..255] of Boolean;   // Holds keystrokes
  FPSCount : Integer = 0;            // Counter for FPS
  ElapsedTime : Integer;             // Elapsed time between frames

  // Textures
  WaterTexture : glUint;

  // User vaiables
  RainInterval : Integer;
  Viscosity : glFloat;
  Position : Array[0..GridSize, 0..GridSize] of glFloat;
  Velocity : Array[0..GridSize, 0..GridSize] of glFloat;

  Vertex : Array[0..GridSize, 0..GridSize] of TglCoord;
  Normals:array [0..GridSize, 0..GridSize] of TglCoord;

  xAngle, yAngle : glFloat;

var
  foInMain             : TfoInMain;
  Needformat,i,x,y      : integer;
  bufc                  : array [1..512]of comp;
  energ,Energ1,Energ2,Energ3  : array[1..128]of integer;
  CurSampl              : integer=0;
  k1,k2,l3,max:integer;
  wndClass : TWndClass;         // Window class
  dwStyle : DWORD;              // Window styles
  dwExStyle : DWORD;            // Extended window styles
  dmScreenSettings : DEVMODE;   // Screen settings (fullscreen, etc...)
  PixelFormat : GLuint;         // Settings for the OpenGL rendering
  h_Instance : HINST;           // Current instance
  pfd : TPIXELFORMATDESCRIPTOR;  // Settings for the OpenGL window
  DC:hdc;

procedure FFTR(buf:array of comp);stdcall; external 'fftc.dll';

implementation

{$R *.DFM}
procedure glBindTexture(target: GLenum; texture: GLuint); stdcall; external opengl32;

{------------------------------------------------------------------}
{  Function to convert int to string. (No sysutils = smaller EXE)  }
{------------------------------------------------------------------}

function IntToStr(Num : Integer) : String;  // using SysUtils increase file size by 100K
begin
  Str(Num, result);
end;


procedure DrawWater;
var I, J : Integer;
    VectLength : glFloat;
begin
  // Calculate new velocity
  For I :=2 to GridSize-2 do
    For J :=2 to GridSize-2 do
      Velocity[I, J] := Velocity[I, J] + (Position[I, J] -
              (4*(Position[I-1,J] + Position[I+1,J] + Position[I,J-1] + Position[I,J+1]) +  // left, right, above, below
              Position[I-1,J-1] + Position[I+1,J-1] + Position[I-1,J+1] + Position[I+1,J+1])/25) / 7;  // diagonally across

  // Calculate the new ripple positions
  For I:=2 to GridSize-2 do
    For J:=2 to GridSize-2 do
    Begin
      Position[I, J] :=
      foInMain.image1.Picture.Bitmap.Canvas.Pixels[round(i*(500/GridSize)),
                        round(j*(128/GridSize))]/800;
//      Velocity[I, J] := Velocity[I, J] * Viscosity;
    End;

  // Calculate the new vertex coordinates
  For I :=0 to GridSize do
    For J :=0 to GridSize do
    begin
      Vertex[I, J].X :=(I - GridSize/2)/GridSize*5;
      Vertex[I, J].Y :=(Position[I, J] / 1024)/GridSize*3;
      Vertex[I, J].Z :=(J - GridSize/2)/GridSize*5;
    end;

  // Calculate the new vertex normals.
  // Do this by using the points to each side to get the right angle
  For I :=0 to GridSize do
  begin
    For J :=0 to GridSize do
    begin
      If (I > 0) and (J > 0) and (I < GridSize) and (J < GridSize) then
      begin
        with Normals[I, J] do
        begin
          X := Position[I+1, J] - Position[I-1,J];
          Y := -2048;
          Z := Position[I, J+1] - Position[I, J-1];

          VectLength :=sqrt(x*x + y*y + z*z);
          if VectLength <> 0 then
          begin
            X :=X/VectLength;
            Y :=Y/VectLength;
            Z :=Z/VectLength;
          end;
        end;
      end
      else
      begin
        Normals[I, J].X :=0;
        Normals[I, J].Y :=1;
        Normals[I, J].Z :=0;
      end;
    end;
  end;

  // Draw the water texture
  glBindTexture(GL_TEXTURE_2D, WaterTexture);
  For J :=0 to GridSize-1 do
  begin
    glBegin(GL_QUAD_STRIP);
      for I :=0 to GridSize do
      begin
        glNormal3fv(@Normals[I, J+1]);
        glTexCoord2f(I/GridSize, (J+1)/GridSize);
        glVertex3fv(@Vertex[I, J+1]);
        glNormal3fv(@Normals[I, J]);
        glTexCoord2f(I/GridSize, J/GridSize);
        glVertex3fv(@Vertex[I, J]);
      end;
    glEnd;
  end;
end;



{------------------------------------------------------------------}
{  Function to draw the actual scene                               }
{------------------------------------------------------------------}
procedure glDraw();
VAR  ps : TPaintStruct;

begin
 // BeginPaint(h_wnd, ps);

  glClear(GL_COLOR_BUFFER_BIT or GL_DEPTH_BUFFER_BIT);    // Clear The Screen And The Depth Buffer
  glLoadIdentity();                                       // Reset The View

  glTranslatef(0.0,0.2,-4.5);

  glRotatef(xAngle, 1, 0, 0);
  glRotatef(yAngle, 0, 1, 0);

  glColor3f(0.85, 1, 0.85);
  DrawWater;
//  endPaint(h_wnd, ps);
  SwapBuffers(DC);
end;


{------------------------------------------------------------------}
{  Initialise OpenGL                                               }
{------------------------------------------------------------------}
procedure glInit();
var I, J : Integer;
begin
  glClearColor(0.9, 0.9, 0.9, 0.0); 	   // Black Background
  glShadeModel(GL_SMOOTH);                 // Enables Smooth Color Shading
  glClearDepth(1.0);                       // Depth Buffer Setup
  glEnable(GL_DEPTH_TEST);                 // Enable Depth Buffer
  glDepthFunc(GL_LESS);		           // The Type Of Depth Test To Do
  glBlendFunc(GL_SRC_COLOR, GL_ONE);

  glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);   //Realy Nice perspective calculations

  glEnable(GL_TEXTURE_2D);               // Enable Texture Mapping
  LoadTexture('reflection.bmp', WaterTexture);    // Load the Texture

  // enable spherical environment maping
 // glEnable(GL_BLEND);
  glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP);
  glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP);
  glEnable(GL_TEXTURE_GEN_S);
  glEnable(GL_TEXTURE_GEN_T);

  Viscosity :=0.96;
  For I :=0 to GridSize do
  begin
    For J :=0 to GridSize do
    begin
      Position[I, J] :=0;
      Velocity[I, J] :=0;
    end;
  end;

  xAngle :=15;
  yAngle :=60;
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

procedure TfoInMain.SpeedButton7Click(Sender: TObject);
begin
  close;
end;

procedure TfoInMain.CaptureFilledBuffer(Sender: TObject);
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
  if cursampl=1 then image:=image2;
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

procedure TfoInMain.FormClose(Sender: TObject; var Action: TCloseAction);
begin
     foInMain.Release;
     foInMain := nil;
end;

procedure RunSQL(q:TADOquery;close:boolean);
begin
      try
        q.Open;
      except
        on EOleException do q.Active:=false;
        on EDatabaseError do q.Active:=false;
      end;
     if close then q.Active:=false;
     q.SQL.SaveToFile('db\1.sql');
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

procedure glResizeWnd(Width, Height : Integer);
begin
  if (Height = 0) then                // prevent divide by zero exception
    Height := 1;
  glViewport(0, 0, Width, Height);    // Set the viewport for the OpenGL window
  glMatrixMode(GL_PROJECTION);        // Change Matrix Mode to Projection
  glLoadIdentity();                   // Reset View
  gluPerspective(45.0, Width/Height, 1.0, 100.0);  // Do the perspective calculations. Last value = max clipping depth

  glMatrixMode(GL_MODELVIEW);         // Return to the modelview matrix
  glLoadIdentity();                   // Reset View
end;

Procedure SetDCPixelFormat;
var
  nPixelFormat: Integer;
  pfd: TPixelFormatDescriptor;
begin
  FillChar(pfd, SizeOf(pfd),0);
  with pfd do begin
    nSize     := sizeof(pfd);                               // Size of this structure
    nVersion  := 1;                                         // Version number
    dwFlags   := PFD_DRAW_TO_WINDOW or
                 PFD_SUPPORT_OPENGL or
                 PFD_DOUBLEBUFFER;                          // Flags
    iPixelType:= PFD_TYPE_RGBA;                             // RGBA pixel values
    cColorBits:= 24;                                        // 24-bit color
    cDepthBits:= 32;                                        // 32-bit depth buffer
    iLayerType:= PFD_MAIN_PLANE;                            // Layer type
  end;
  nPixelFormat := ChoosePixelFormat(DC, @pfd);
  SetPixelFormat(DC, nPixelFormat, @pfd);
  DescribePixelFormat(DC, nPixelFormat, sizeof(TPixelFormatDescriptor), pfd);
end;

procedure TfoInMain.FormCreate(Sender: TObject);
var   Reg: TRegistry;
      s:string;
      us_id:string;
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

  left:=0;
  top:=0;
  height:=screen.height
  ;
  width:=screen.width;
  speedbutton7.left:=width-speedbutton7.Width-5;
  Image1.Canvas.Brush.Color:=clwhite;
  Image1.Canvas.Rectangle(0,0,Image1.width,Image1.Height);
  GetSpectrPicture('test1.wav',image1,3);


  ADOquery1.Active:=false;
  ADOquery1.SQL.Clear;
  ADOquery1.SQL.add('select * from userinfo where (deleted=0) and (login="'+edit2.Text+'")');
  RunSQL(ADOquery1,false);
  us_id:=ADOquery1.FieldByName('user_id').asstring;

  ADOquery1.Active:=false;
  ADOquery1.SQL.Clear;
  ADOquery1.SQL.add('select * from reg where (deleted=0) and (user_id='+us_id+')');
  RunSQL(ADOquery1,false);

  ADOquery1.First;
  while not ADOquery1.eof do
  with ADOquery1 do
   begin
     if ADOquery1.FieldByName('number').asinteger=1 then
       begin
         s:=ADOquery1.FieldByName('spectr').AsString;
         stringtobyte(s,energ1);
       end;
     if ADOquery1.FieldByName('number').asinteger=2 then
       begin
         s:=ADOquery1.FieldByName('spectr').AsString;
         stringtobyte(s,energ2);
       end;
     if ADOquery1.FieldByName('number').asinteger=3 then
       begin
         s:=ADOquery1.FieldByName('spectr').AsString;
         stringtobyte(s,energ3);
       end;
     ADOquery1.Next;
   end;


  h_wnd:=panel1.Handle;

  DC := GetDC(h_wnd);
  SetDCPixelFormat;
  H_RC := wglCreateContext(DC);
  wglMakeCurrent(DC, H_RC);

//  gluPerspective(45.0, panel1.Width/panel1.Height, 1.0, 100.0);  // Do the perspective calculations. Last value = max clipping depth
//  glViewport(0, 0, panel1.Width, panel1.Height);    // Set the viewport for the OpenGL window
  glMatrixMode(GL_PROJECTION);        // Change Matrix Mode to Projection
  glLoadIdentity();                   // Reset View

  glMatrixMode(GL_MODELVIEW);         // Return to the modelview matrix
  glLoadIdentity();                   // Reset View
  glResizeWnd(panel1.Width, panel1.Height);
  glinit;

end;

procedure TfoInMain.Image5MouseDown(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
begin
  if sender = image5 then cursampl:=1;
  if cursampl<>0 then begin
  deletefile('test.wav');

    //--------

    FCapture.Free;
    FCapture := TSoundCaptureStream.Create(nil);
    FWaveStream := TWaveFileStream.Create('test.wav', fmCreate);
    with FCapture.SupportedFormats[8] do
    FWaveStream.SetPCMFormat(22050, 8, 1);
    FWaveStream.Open(True);

    FCapture.OnFilledBuffer := CaptureFilledBuffer;

    FCapture.CaptureFormat := 8;
    FCapture.Start;
   end;
end;

procedure TfoInMain.Image5MouseUp(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);

var spectr:array[1..128]of integer;
    i1,i2,i3,max:real;
    i:integer;
    image:timage;
       f:file;
begin
  if FCapture<>nil then
  FCapture.Stop;
  FWaveStream.Free; FWaveStream := nil;

  if cursampl=1 then begin image:=image2;end;

  getspectr('test.wav',spectr);

  Image.Canvas.Brush.Color:=clwhite;
  Image.Canvas.Rectangle(0,0,Image.width,Image.Height);
  Image.Canvas.MoveTo(0,128);
  for i:=1 to 128 do
   begin
    Image.Canvas.LineTo(i,128-spectr[i]);
    energ[i]:=spectr[i];
   end;
  cursampl:=0;

  Image1.Canvas.Brush.Color:=clwhite;
  Image1.Canvas.Rectangle(0,0,Image1.width,Image1.Height);

  GetSpectrPicture('test.wav',image1,6);

     max:=0;
     i1:=calc_fxy(energ1,energ);
     if i1>max then max:=i1;
     i2:=calc_fxy(energ2,energ);
     if i2>max then max:=i2;
     i3:=calc_fxy(energ3,energ);
     if i3>max then max:=i3;
     label4.caption:=inttostr(round(i1*100));
     label5.caption:=inttostr(round(i2*100));
     label6.caption:=inttostr(round(i3*100));
end;

procedure TfoInMain.SpeedButton7MouseDown(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
begin
close;
end;

procedure TfoInMain.Timer1Timer(Sender: TObject);
begin
//  Velocity[random(GridSize-3)+2, random(GridSize-3)+2] :=1060;
  yAngle :=yangle+0.5;
glDraw();

end;

end.
