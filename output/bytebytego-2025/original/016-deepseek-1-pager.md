# 016 - DeepSeek 1-Pager

- Source: ByteByteGo Big Archive System Design 2025
- PDF pages: 38-39
- Figures: 1

## Figures

![DeepSeek 1-Pager - figure 1](../assets/016/figure-01.png)

## Original Extracted Text

It is said to have developed a powerful AI model at a remarkably low cost, approximately $6 million
for the final training run. In January 2025, it is said to have released its latest reasoning-focused
model known as DeepSeek R1.

The release made it the No. 1 downloaded free app on the Apple Play Store.

Most AI models are trained using supervised fine-tuning, meaning they learn by mimicking large
datasets of human-annotated examples. This method has limitations.

DeepSeek R1 overcomes these limitations by using Group Relative Policy Optimization (GRPO), a
reinforcement learning technique that improves reasoning efficiency by comparing multiple possible
answers within the same context.

Some facts about DeepSeek's R1 model are as follows:

   1. DeepSeek-R1 uses a Mixture-of-Experts (MoE) architecture with 671 billion total parameters,
       activating only 37 billion parameters per task.

   2. It employs selective parameter activation through MoE for resource optimization.

   3. The model is pre-trained on 14.8 trillion tokens across 52 languages.

   4. DeepSeek-R1 was trained using just 2000 Nvidia GPUs. By comparison, ChatGPT-4 needed
       approximately 25K Nvidia GPUs over 90-100 days.

   5. The model is 85-90% more cost-effective than competitors.

   6. It excels in mathematics, coding, and reasoning tasks.

   7. Also, the model has been released as open-source under the MIT license.

Over to you: Have you tried DeepSeek?
