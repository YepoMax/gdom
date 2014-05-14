/* === Javascript sample ===

Used for testing purpose : converting Javascript to Python code.

Context :
	sampleNS.xml is loaded in the variable document
	document is an XML Document node.

*/



function nextSibling( node ){ // Find the next sibling node of the same type
	
	while(node.nextSibling && node.nextSibling.nodeType != node.nodeType){
		node = node.nextSibling;
	}
	
	return node.nextSibling;
	
}

function nextNode( node ){ // Returns the very next node

	if (!node) return node;
	if (node.hasChildNodes()) return node.childNodes[0];
	else return nextNode(node.parentNode);

}

function main(){
	// Do some changes to document

	var books = document.getElementsByTagName("book");
	
	for(var i = 0; i < books.length; i++){
	
		var book = books[i];
		
		// Explicit language on title
		book.getElementsByTagNameNS("http://www.oxforddictionaries.com/", "title")[0].firstChild.data += " (ENGLISH VERSION)";
		book.getElementsByTagNameNS("http://www.oxforddictionaries.com/", "title")[0].firstChild.data += " (FRENCH VERSION)";
		
		prices = book.getElementsByTagNameNS("*", "price");
		
		for(var p = 0; p < prices.length; p++){
		
			// Add 5.87 € or $ to price.
			var price = parseInt(prices[p].firstChild.data.slice(0,5)) + 5.87;
			prices[p].firstChild.data = price + prices[p].firstChild.data.slice(5);
		
		}
	
	}

}

main();
