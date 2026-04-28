
import 'package:flutter/material.dart';
import 'package:razorpay_flutter/razorpay_flutter.dart';

class PaymentPage extends StatefulWidget {
  @override
  _PaymentPageState createState() => _PaymentPageState();
}

class _PaymentPageState extends State<PaymentPage> {
  late Razorpay _razorpay;

  @override
  void initState() {
    super.initState();
    _razorpay = Razorpay();
    _razorpay.on(Razorpay.EVENT_PAYMENT_SUCCESS, _success);
    _razorpay.on(Razorpay.EVENT_PAYMENT_ERROR, _error);
  }

  void _pay() {
    var options = {
      'key': 'YOUR_KEY',
      'amount': 50000,
      'name': 'NidhiRaj Ventures',
      'description': 'Order Payment'
    };
    _razorpay.open(options);
  }

  void _success(PaymentSuccessResponse r) {
    print("Success");
  }

  void _error(PaymentFailureResponse r) {
    print("Error");
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Payment")),
      body: Center(
        child: ElevatedButton(onPressed: _pay, child: Text("Pay Now")),
      ),
    );
  }
}
