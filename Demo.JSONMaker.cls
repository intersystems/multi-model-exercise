Class Demo.JSONMaker Extends (%Persistent,%JSON.Adaptor)
{

ClassMethod fromJSON(j as %String) As %Integer

{
	w "test"
	set e = ..%New()
	do e.%JSONImport(j)
 	set e.ID = 0
 	
	do e.%Save()
	
	
	
	
	return 1
}


}
