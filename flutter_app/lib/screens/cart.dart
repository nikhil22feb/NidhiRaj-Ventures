
import 'package:flutter/material.dart';
import '../services/payment.dart';

class CartScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context){
    return Scaffold(
      appBar: AppBar(title: Text('Cart')),
      body: Center(
        child: ElevatedButton(
          onPressed: (){
            PaymentService().pay();
          },
          child: Text('Checkout & Pay'),
        ),
      ),
    );
  }
}
