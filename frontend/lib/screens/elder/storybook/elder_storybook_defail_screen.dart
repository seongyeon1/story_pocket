import 'package:flutter/material.dart';
import 'package:my_project/models/story.dart';

class ElderStorybookDefailScreen extends StatelessWidget {
  final Story story;
  const ElderStorybookDefailScreen({super.key, required this.story});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(story.title),
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
      body: Container(
        padding: const EdgeInsets.symmetric(horizontal: 20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("작성자 : ${story.author}"),

            //이야기
            Text(story.story),
          ],
        ),
      ),
    );
  }
}
