
import 'package:flutter/material.dart';
import 'home.dart';

class LoginScreen extends StatelessWidget {
  final u = TextEditingController();
  final p = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Login')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(children: [
          TextField(controller: u, decoration: InputDecoration(labelText: 'Username')),
          TextField(controller: p, decoration: InputDecoration(labelText: 'Password'), obscureText: true),
          SizedBox(height: 16),
          ElevatedButton(
            onPressed: () {
              Navigator.push(context, MaterialPageRoute(builder: (_) => HomeScreen()));
            },
            child: Text('Login')
          )
        ]),
      ),
    );
  }
}
