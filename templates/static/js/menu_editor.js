sections = [];
items = [];
function new_section(name){
	name = delete_preceeding_char(name,' ');
	name = proper_case(name);
	if (sections.indexOf(name) == -1
		&& name != ''){
		sections.push(name);
		id = sections.length-1;
		items[id] = [];
		$('#section-container').append(get_section_template(id));
		$('#section'+id).fadeIn('slow');
	}else{
		$('#invalid-section').fadeIn();
	}
}
function count_sections(){
	count = 0;
	for (i = 0; i < sections.length; i++){
		if (sections[i] != ""){
			count++;
		}
	}
	return count;
}
function count_items(id){
	count = 0;
	for (i = 0; i < items[id].length; i++){
		if (items[id][i] != []){
			count++;
		}
	}
	return count;
}
function remove_section(id){
	sections[id] = '';
	items[id] = [];
	$('#section' + id).fadeOut(function(){$(this).remove();});
}
function remove_item(section_id,id){
	items[section_id][id] = [];
	$('#section' + section_id + '-item' + id).fadeOut(function(){$(this).remove();});
}
function new_item(name,desc,price,section_id){
	name = delete_preceeding_char(name,' ');
	if (price == 0){
		if (!confirm("This item is free! Are you sure you want to continue?")){
			return;
		}
	}else{
		price = delete_preceeding_char(price,'0');
	}
	if (name != '' && desc != ''){
		items[section_id].push([name,desc,price]);
		id = items[section_id].length-1;
		$('#section' + section_id + '-contents').append(get_item_template(name,desc,price,id,section_id));
		$('#section' + section_id + '-item' + id).fadeIn('slow');
	}else{
		if (name == ''){
			$('#section' + section_id + '-invalid-item').fadeIn();
		}
		if (desc == ''){
			$('#section' + section_id + '-invalid-desc').fadeIn();
		}
	}
}
function get_item_template(name,desc,price,item_id,section_id){
	var template = 
		'<div style="display:none;" class="item" id="section%section_id%-item%item_id%">' + 
			'<div class="item-title">' +
				'%name%' + 
				'<input type="image" class="edit-delete-element" src="static/img/cross.png" width="12" height="12" onclick="remove_item(%section_id%,%item_id%)">' + 
			'</div>' +	
			'<div class="item-contents">' + 
				'£%price%' + 
				'<br>' + 
				'%desc%' +
			'</div>' + 
			'<hr style="border-width: 1px;">' +
		'</div>';
	template = template.replace(/%section_id%/g,section_id);
	template = template.replace(/%name%/g,proper_case(name));
	template = template.replace(/%item_id%/g,item_id);
	template = template.replace(/%price%/g,price);
	template = template.replace(/%desc%/g,desc);
	return template;
}
function edit_section(id){
	$('#section' + id + '-title').hide();
	$('#section' + id).prepend(
		'<div style="display:none;padding: 0px 0px 10px 0px;" id="section' + id + '-edit-title">' +
			'<input type="text" style="font-size:75%;" id="section' + id + '-edit-title-input" value="' + proper_case(sections[id]) + '" onfocus="$(\'#section' + id + '-invalid-edit\').hide();" required>' + 
			'<input type="button" value="Update" onclick="update_section(' + id + ',$(\'#section' + id + '-edit-title-input\').val())">' +
			'<br>' +
			'<p id="section' + id + '-invalid-edit" style="font-size:75%;display:none;color:rgb(0,0,0);">Invalid section name.</p>' +
		'</div>'
		);
	$('#section' + id + '-edit-title').fadeIn('slow');
}
function update_section(id,new_name){
	new_name = delete_preceeding_char(new_name,' ');
	new_name = proper_case(new_name);
	if (sections.indexOf(new_name) == -1
		|| sections.indexOf(new_name) == id){
		$('#section' + id + '-title-name').html(new_name);
		$('#section' + id + '-edit-title').fadeOut(function(){$(this).remove();
			$('#section' + id + '-title').fadeIn();});
		sections[id] = new_name;
	}else{
		$('#section' + id + '-invalid-edit').fadeIn('slow');
	}
}
function get_section_template(id){
	var template = 
	'<div style="display:none;" class="section" id="section%id%">' + 
		'<div class="section-title" id="section%id%-title">' + 
			'<a id="section%id%-title-name">' + 
			'%name%' + 
			'</a>' +
			'<input type="image" class="edit-delete-element" src="static/img/cross.png" width="12" height="12" onclick="remove_section(%id%)">' + 
			'<input type="image" class="edit-delete-element" src="static/img/edit.png" width="12" height="12" onclick="edit_section(%id%)">' + 
		'</div>' + 
		'<div class="section-contents" id="section%id%-contents">' +
		'</div>' + 
		'<div id="section%id%-new-item" class="new-item">' + 
			'New item:' + 
			'<br>' + 
			'<div class="item-input">' + 
				'<div class="item-input-label">Name:</div>' + 
				'<input style="width:100%;" type="text" id="section%id%-item-name" onfocus="$(\'#section%id%-invalid-item\').hide()">' + 
			'</div>' +
			'<div class="item-input">' + 
				'<div class="item-input-label">Description:</div>' + 
				'<textarea style="resize:none;width:100%;" id="section%id%-item-description" onfocus="$(\'#section%id%-invalid-desc\').hide()" />' + 
			'</div>' +
			'<div class="item-input">' + 
				'<div class="item-input-label">Price:</div>' + 
				'<input type="number" style="width:100%;" value="0" min="0" id="section%id%-item-price">' + 
			'</div>' +
			'<br>' + 
			'<input type="button" id="section%id%-add-item" value="Add"' + 
				'onclick="new_item('+
					'$(\'#section%id%-item-name\').val(),' + 
					'$(\'#section%id%-item-description\').val(), ' +
					'$(\'#section%id%-item-price\').val(),' + 
					'\'%id%\')">' + 
			'<p id="section%id%-invalid-item" style="font-size:75%;display:none;color:rgb(0,0,0);">Invalid item name.</p>' +
			'<p id="section%id%-invalid-desc" style="font-size:75%;display:none;color:rgb(0,0,0);">Invalid description.</p>' +
		'</div>' + 
		'<hr style="border-width: 3px;">' +
	'</div>';
	template = template.replace(/%id%/g,id);
	template = template.replace(/%name%/g,proper_case(sections[id]));
	return template;
}
function delete_preceeding_char(str, chr){
	var len = str.length;
	for (i = 0; i < len; i++){
		if (str.substring(0, 1) == chr){
			str = str.substring(1);
		}else{
			return str;
		}
	}
	return null;
}
function convert_to_JSON(){
	temp_sections = [];
	temp_items = [];
	for (k = 0; k < sections.length; k++){
		if (sections[k] != ''){
			temp_sections.push(sections[k]);
			idx = temp_sections.length-1;
			sec_items = [];
			for (l = 0; l < items[k].length; l++){
				if (items[k][l].length > 0){
					sec_items.push(items[k][l]);
				}
			}
			temp_items.push(sec_items);
		}
	}
	
	var JSON = '{ "menu": [{ "category": [';
	for (i = 0; i < temp_sections.length; i++){
		JSON += '{ "title": "' + temp_sections[i] + '",' +
			'"category_id": ' + (i+1) + ',' +
			'"items": [';
		for (j = 0; j < temp_items[i].length; j++){
			JSON += '{"item_title": "' + temp_items[i][j][0] + '",' +
				'"item_id": "' + (j+1) + '",' +
				'"item_description": "' + temp_items[i][j][1] + '",' +
				'"item_price": ' + temp_items[i][j][2] + '}';
			if (j < temp_items[i].length-1) JSON += ',';
		}
		JSON += ']}';
		if (i < temp_sections.length-1) JSON += ',';
	}
	JSON += ']}]}';
	console.log(JSON);
}
function proper_case(str) {
	str = str.toLowerCase().split(' ').map(function(word) {
		return (word.charAt(0).toUpperCase() + word.slice(1));
	});
	return str.join(' ');
}
function JSON_to_form(menu){
	$('#section-container').html('');
	
	temp_sections = [];
	temp_items = [];
	
	try {
		section_json = JSON.parse(menu).menu[0].category;
	} catch (e) {
		return false;
	}
	num_sections = section_json.length;
	
	for (i = 0; i < num_sections; i++){
		temp_sections.push(section_json[i].title);
		item_json = section_json[i].items;
		temp_items[i] = [];
		for (j = 0; j < item_json.length; j++){
			temp_items[i].push([item_json[j].item_title,item_json[j].item_description,item_json[j].item_price]);
		}
	}
	
	sections = [];
	items = [];
	for (k = 0; k < num_sections; k++){
		new_section(temp_sections[k]);
		for (l = 0; l < temp_items[k].length; l++){
			new_item(temp_items[k][l][0],temp_items[k][l][1],temp_items[k][l][2].toString(),k);
		}
	}
	return true;
}

