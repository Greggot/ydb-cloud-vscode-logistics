function Automobile(obj) {
    this.id = obj.id;
    this.model = obj.model;
    this.name = obj.name;
}
Automobile.prototype = {
    constructor: Automobile,
    print: function(){
        console.log(this.to_string());
    },
    to_string: function(){
        return "Id: " + this.id + ", mark: " + this.model + ", name: " + this.name;
    },
    to_table_entry: function(){
        return '<tr><td>' + 
        this.id + '</td><td>' + 
        this.model + '</td><td>' + 
        this.name + '</td></tr>'
    }
}