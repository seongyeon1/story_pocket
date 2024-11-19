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
        padding: const EdgeInsets.symmetric(horizontal: 30),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Text("작성자 : ",
                    style: TextStyle(fontWeight: FontWeight.bold)),
                Text(story.author)
              ],
            ),

            const SizedBox(height: 20),

            //이야기 작성란
            Text(story.story),

            //추천
            Center(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  IconButton(
                    iconSize: 50,
                    onPressed: () {},
                    icon: const Icon(Icons.thumb_up),
                  ),
                  Text("추천수 : ${story.numberOfView}"),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }
}
