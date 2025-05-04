import openai
import time
import logging

class GPT4:

    def __init__(self, max_tokens=1024, temperature=0.0, logprobs=None, n=1, engine='gpt-4o-2024-08-06',
        frequency_penalty=0, presence_penalty=0, stop=None, rstrip=False, **kwargs):

        self.max_tokens = max_tokens
        self.temperature = temperature
        self.rstrip = rstrip
        self.engine = engine
        self.client = openai.OpenAI(api_key='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')

    def complete(self, prompt):

        if self.rstrip:
            prompt = prompt.rstrip()
        retry_interval_exp = 1

        while True:
            try:
                response = self.client.chat.completions.create(
                    model=self.engine,
                    response_format={ "type": "json_object" },
                    messages=[
                        {"role": "system", "content": "You are an expert in control engineering design."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                return response.choices[0].message.content
            except openai.RateLimitError:
                logging.warning("Rate limit error. Retrying...")
                time.sleep(max(4, 0.5 * (2 ** retry_interval_exp)))
                retry_interval_exp += 1
            except openai.APIConnectionError:
                logging.warning("API connection error. Retrying...")
                time.sleep(max(4, 0.5 * (2 ** retry_interval_exp)))
                retry_interval_exp += 1
