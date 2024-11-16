import 'package:flutter/material.dart';

class ElderContantsScreen extends StatefulWidget {
  const ElderContantsScreen({super.key});

  @override
  State<ElderContantsScreen> createState() => _ElderContantsScreenState();
}

class _ElderContantsScreenState extends State<ElderContantsScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        actions: [
          IconButton(
            onPressed: () {},
            icon: const Icon(Icons.monetization_on_rounded),
          ),
          IconButton(
            onPressed: () {},
            icon: const Icon(Icons.notifications),
          ),
          IconButton(
            onPressed: () {},
            icon: const Icon(Icons.account_circle_rounded),
          )
        ],
      ),
      body: const Text("asds"),
    );
  }
}
