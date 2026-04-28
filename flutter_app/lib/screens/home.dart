
import 'package:flutter/material.dart';
import 'cart.dart';

class HomeScreen extends StatelessWidget {
  final products = [
    {"name":"Chopper","price":249},
    {"name":"Rack","price":199}
  ];

  @override
  Widget build(BuildContext context){
    return Scaffold(
      appBar: AppBar(title: Text('Products')),
      body: ListView(
        children: products.map((p)=>ListTile(
          title: Text(p['name'].toString()),
          subtitle: Text("₹${p['price']}"),
          trailing: Icon(Icons.add_shopping_cart),
        )).toList(),
      ),
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.shopping_cart),
        onPressed: ()=>Navigator.push(context, MaterialPageRoute(builder:(_)=>CartScreen())),
      ),
    );
  }
}
