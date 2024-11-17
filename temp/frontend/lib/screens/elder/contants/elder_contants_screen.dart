import 'package:flutter/material.dart';

class ElderStoybookScreen extends StatefulWidget {
  const ElderStoybookScreen({super.key});

  @override
  State<ElderStoybookScreen> createState() => _ElderStoybookScreenState();
}

class _ElderStoybookScreenState extends State<ElderStoybookScreen> {
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
