class StoryCut {
  final int id;
  final String text;
  final String description;
  final String imagePrompt;
  final String imagePath;

  StoryCut({
    required this.id,
    required this.text,
    required this.description,
    required this.imagePrompt,
    required this.imagePath,
  });

  factory StoryCut.fromJson(Map<String, dynamic> json) {
    return StoryCut(
      id: json['id'] as int,
      text: json['text'] as String,
      description: json['description'] as String,
      imagePrompt: json['image_prompt'] as String,
      imagePath: json['image_path'] as String,
    );
  }
}

class Story {
  final String sessionId;
  final String title;
  final String author; // 사용자 이름
  final String storyText;
  final int recommendations;
  final int views;
  final List<StoryCut> cuts;

  Story({
    required this.sessionId,
    required this.title,
    required this.author,
    required this.storyText,
    required this.recommendations,
    required this.views,
    required this.cuts,
  });

  factory Story.fromJson(Map<String, dynamic> json) {
    return Story(
      sessionId: json['session_id'] as String,
      title: json['title'] as String,
      author: json['author'] as String, // 사용자 이름 매핑
      storyText: json['story_text'] as String,
      recommendations: json['recommendations'] as int,
      views: json['views'] as int,
      cuts: (json['cuts'] as List<dynamic>)
          .map((cutJson) => StoryCut.fromJson(cutJson))
          .toList(),
    );
  }
}