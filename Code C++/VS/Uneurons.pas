unit Uneurons;

interface

function Sigmoid(s,a:real):real;

implementation

function Sigmoid(s,a:real):real;
begin
  result:=1/(1+exp(-a*s));
end;

end.
 