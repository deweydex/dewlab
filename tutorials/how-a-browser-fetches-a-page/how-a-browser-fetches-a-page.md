---
title: "How a browser fetches a page"
year: "2026-2027"
version: 2026.09.22.1
context_for: [publish-it, the-two-loops, the-inspector]
---

# How a browser fetches a page

What happens between typing a web address and seeing a page? Three
pages give part of the answer: [Publishing your site with GitHub
Pages](tutorial:publish-it), [Saving and publishing a
change](tutorial:the-two-loops) and [Looking inside a page with the
inspector](tutorial:the-inspector). This page follows one visit from
start to end. It is background reading. You do not need it to finish
those pages, but it can help you see why a page is sometimes missing,
or sometimes an old version.

On this page we:

- read the parts of a web address
- see how a browser finds the right computer
- follow a request, and the response that comes back
- see why one page takes more than one request
- see why a refresh can still show an old page
- watch all of this in the inspector's **Network** tab

## The parts of a web address

Here is the address of an About page on a GitHub Pages site:

```text
https://janedoe.github.io/web/about.html
```

It has three parts.

- `https://` says how the browser and the other computer talk to each
  other. The `s` stands for *secure*. Nobody in between can read or
  change what they send.
- `janedoe.github.io` is the *domain name*. A domain name is the name
  of a website, which leads the browser to the computer that holds it.
- `/web/about.html` is the *path*. A path says which file we want,
  on that site.

A domain name reads from right to left, from the biggest part to the
smallest. Every domain name ends with one of a fixed set of endings,
such as `com`, `ie` or `io`. `github.io` belongs to GitHub. And `janedoe.github.io`
is one of many names that GitHub gives, one for each account that
publishes a site.

## Finding the right computer

Computers on the internet find each other by number. Each one has an
*IP address*, a number like `185.199.108.153`. So how does a browser
turn a name into a number?

It asks *DNS*, the Domain Name System. DNS is like the contacts list on
a phone. We look up a name, and it gives us the number to call. The
browser keeps the answer for a while, so it does not ask again for
every page on the same site.

Many sites share the same computers. Every GitHub Pages site is served
by GitHub's own computers. So the browser also sends the domain name
along with its request, and GitHub uses it to decide which site to
answer from.

## A request and a response

A *server* is a computer that waits for requests and answers them. Once
the browser knows where GitHub's server is, it sends a *request*. The
request asks for one file, by its path. The server sends back a
*response*: a short status, and then the file itself.

Here is the whole visit, with time running down the picture:

![A diagram with three columns: your browser, DNS (the address book), and GitHub's server (where your files are). Time runs down the page. First, the browser asks DNS: where is janedoe.github.io? DNS answers: at 185.199.108.153. Next, the browser sends a request to GitHub's server: GET /web/about.html. The server sends a response: 200 OK, here is the HTML. The HTML names a stylesheet, so the browser sends a second request: GET /web/styles.css. The server answers: 200 OK, here is the CSS. At the bottom, the browser draws the page.](request-and-response.svg)

`GET` is the word a browser uses to ask for a file. The rules for
these requests and responses are called *HTTP*. The `http` in
`https://` comes from this name.

The status is a number, the *status code*, with a few words after it.
Two of them are very common:

| Status code | Meaning | When we see it |
|---|---|---|
| `200 OK` | Here is the file. | Every time a page loads as it should. |
| `404 Not Found` | There is no file at this path. | A misspelt address, a file with a different name, or a site that is not published yet. |

Codes that start with `5`, such as `500`, mean the server itself had a
problem. Those are rare on GitHub Pages, and there is nothing in your
own files to fix for them.

A GitHub Pages site sends your files as they are, the same files you
see in your repository. When you commit, GitHub copies the new version
of your files onto the computers that serve your site. This is why
you wait a minute or two in [the second
loop](tutorial:the-two-loops#waiting-for-the-site-to-rebuild).

## One page, many requests

The first response holds only the HTML. As the browser reads it, it
finds the names of other files the page needs: the stylesheet in the
`<link>` line, each picture in an `<img>`, each script. It sends a new
request for each one.

Each of those requests can fail on its own. If the stylesheet's name is
misspelt, the page still arrives, but the request for the stylesheet
gets a `404`. The page appears with no styles, and the inspector's
**Console** tab shows an error that names the missing file. So an error
in the Console is often a request that got a `404`.

## Why a refresh can show an old page

A browser keeps copies of the files it has fetched, in a store called
the *cache*. When we visit the same page again, it can use its copy,
and the page opens faster. The server's response says how long a copy
may be kept.

Sometimes we might push a change, wait for the rebuild, refresh, and
still see the old version. The browser may be using its cached copy.
A *hard refresh* asks the server for fresh copies of everything. In
Chrome, Edge and Firefox, the keys are:

- `Ctrl+Shift+R` on Windows and Linux
- `Cmd+Shift+R` on a Mac

Opening the address in a private window works too, because a private
window starts with an empty cache.

## Seeing it in the inspector

The inspector has a tab for all of this: the **Network** tab. It lists
every request the page makes, in the order the browser made them.

You could try it on your own published site:

1. Open your site, and open the inspector.
2. Choose the **Network** tab. It may be empty, because it only records
   while it is open.
3. Refresh the page. One row appears for each request. Can you find the
   rows for your HTML file and for `styles.css`?
4. Find the **Status** column. What number does each row show?
5. Now add `nothing-here.html` to the end of your address, and open it.
   What status does the first row show now?

Some rows in step 4 may show `304` instead of `200`. That code means
"the copy you already have has not changed", so the browser uses the
copy in its cache.

In Chrome and Edge, the Network tab has a **Disable cache** box. While
it is ticked, and the inspector is open, the browser fetches fresh
copies every time. Firefox has the same box, in the same tab.

## What we have now

We can now follow a visit to a web page, from the address to the page
on the screen, and say where it can go wrong.

| Word | Meaning | Example |
|---|---|---|
| *domain name* | The name of a website, which leads the browser to the computer that holds it | `janedoe.github.io` |
| *path* | The part of an address after the domain name, which says which file we want | `/web/about.html` |
| *IP address* | The number a computer has on the internet | `185.199.108.153` |
| *DNS* | The system that turns a domain name into an IP address | the browser asks where `janedoe.github.io` is |
| *server* | A computer that waits for requests and answers them | GitHub's computers, for a GitHub Pages site |
| *request* | A message from the browser that asks for one file | `GET /web/about.html` |
| *response* | The server's answer: a status code, then the file | `200 OK`, then the HTML |
| *status code* | The number at the start of a response, which says how the request went | `200`, `404` |
| *HTTP* | The rules for requests and responses on the web | the `http` in `https://` |
| *cache* | The browser's store of files it has already fetched | an old copy of `styles.css` |

## Where to read more

CrashCourse (2017). *The Internet: Crash Course Computer Science #29.*
<https://www.youtube.com/watch?v=AEaKrq3SpW8>. It shows what happens between
typing a web address and seeing the page: finding the right computer, and sending
the request across many networks in small packets. Twelve minutes.

Ben Eater (2021). *Why was Facebook down for five hours?*
<https://www.youtube.com/watch?v=-wMU8vmfaYo>. In October 2021, Facebook
could not be found on the internet for five hours. Ben Eater explains why,
using the name lookup this page describes. About thirty minutes, for
readers who want the detail.
