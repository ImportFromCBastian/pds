/** @type {import('tailwindcss').Config} */
module.exports = {
	content: [
		'./src/web/templates/**/*.{html,py}',
		'./src/web/handlers/**/*.{py,html}',
		'./static/**/*.css',
	],
	theme: {
		extend: {},
	},
	plugins: [],
};
