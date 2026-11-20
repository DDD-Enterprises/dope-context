const test = require('node:test');
const assert = require('node:assert/strict');
const { LangChainCodeSplitter } = require('../dist/splitter/langchain-splitter');

for (const language of ['javascript', 'unknown']) {
    test(`splits synthetic ${language} input with metadata`, async () => {
        const source = Array.from({ length: 12 }, (_, i) => `function entry${i}() { return ${i}; }`).join('\n');
        const chunks = await new LangChainCodeSplitter(100, 20).split(source, language, 'synthetic.txt');
        assert.ok(chunks.length > 1);
        for (const chunk of chunks) {
            assert.ok(chunk.content.length > 0 && chunk.content.length <= 100);
            assert.ok(source.includes(chunk.content));
            assert.equal(chunk.metadata.language, language);
            assert.equal(chunk.metadata.filePath, 'synthetic.txt');
            assert.ok(chunk.metadata.startLine >= 1);
            assert.ok(chunk.metadata.endLine >= chunk.metadata.startLine);
        }
    });
}

test('returns no chunks for empty input', async () => {
    assert.deepEqual(await new LangChainCodeSplitter(100, 20).split('', 'javascript'), []);
});
