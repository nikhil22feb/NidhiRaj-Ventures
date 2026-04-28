
import 'package:razorpay_flutter/razorpay_flutter.dart';

class PaymentService {
  final _razorpay = Razorpay();

  void pay(){
    var options = {
      'key': 'YOUR_KEY',
      'amount': 50000,
      'name': 'NidhiRaj Ventures',
      'description': 'Order Payment'
    };
    _razorpay.open(options);
  }
}
